import json
from typing import List
import praw
import logging
from dotenv import load_dotenv
import os
from api.claude import ClaudeChat
from api.fetch_prompt import PromptFetcher
from reddit.reddit_config import LIMIT, ANALYSE_REDDIT_PROMPT

class Reddit:
    def __init__(self):
        load_dotenv()
        reddit_id = os.getenv('REDDIT_ID')
        reddit_secret = os.getenv('REDDIT_SECRET')

        if not reddit_id or not reddit_secret:
            raise ValueError("REDDIT_ID and REDDIT_SECRET must be set in the environment variables.")

        self.reddit = praw.Reddit(
            client_id=reddit_id,
            client_secret=reddit_secret,
            user_agent='myRedditApp/1.0'
        )
        logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

    def analyse_reddit(self):
        with open('content/reddit_api_content.json', 'r', encoding='utf-8') as file:
            reddit_content = json.load(file)
        system_instruction, user_instruction, tools = PromptFetcher.fetch_prompt(ANALYSE_REDDIT_PROMPT, json.dumps(reddit_content))

        filename = input("Enter the filename to save the tweets. Lowercase, no spaces: ").lower().replace(" ", "_")
        file_path = f'content/{filename}.json' 
        ClaudeChat.send_message(file_path, system_instruction, user_instruction, tools)
        print(f"Reddit analysis complete, saved to {file_path}.")  

    def fetch_posts(self, subreddit_names, mode, seen_posts=set(), **kwargs):
        """
        Fetches posts from the specified subreddits and saves them to a JSON file.
        """
        posts_data = []
        for subreddit_name in subreddit_names:
            logging.info(f"Fetching posts from /r/{subreddit_name}...")
            subreddit = self.reddit.subreddit(subreddit_name)
            posts = self._fetch_posts(subreddit, mode, seen_posts, **kwargs)
            for post in posts:
                post_data = {
                    'title': post['title'],
                    'mode': post['mode'].capitalize(),
                    'upvotes': post['upvotes'],
                    'comments': post['comments'],
                    'url': post['url'],
                    'content': post['content']
                }
                posts_data.append(post_data)

        self.write_to_json(posts_data)
        return posts_data
            

    def _fetch_posts(self, subreddit, mode, seen_posts, **kwargs):
        """
        Fetches posts from a subreddit based on the mode and returns their details.
        """
        fetch_method = getattr(subreddit, mode)
        posts_details = []
        if mode in ['top', 'controversial']: 
            for submission in fetch_method(limit=LIMIT, **kwargs):
                if not submission.stickied and submission.id not in seen_posts:
                    posts_details.append(self._get_post_details(submission, mode, seen_posts))
        else:
            for submission in fetch_method(limit=LIMIT):
                if not submission.stickied and submission.id not in seen_posts:
                    posts_details.append(self._get_post_details(submission, mode, seen_posts))
        return posts_details

    def _get_post_details(self, submission, mode, seen_posts):
        """
        Returns a single post's details.
        """
        seen_posts.add(submission.id)
        return {
            "title": submission.title,
            "author": str(submission.author),
            "upvotes": submission.score,
            "comments": submission.num_comments,
            "url": submission.url,
            "content": submission.selftext,
            "mode": mode
        }

    def load_or_create_reddit_channels() -> List[str]:
        """
        Loads Reddit channels from a JSON file or creates the file from user input.
        
        This function first checks if the 'reddit/channels.json' file exists. If it does,
        it loads and offers the user to use these channels. If the user declines or the file
        doesn't exist, it prompts the user to enter a new list of channels as a CSV string,
        saves it to the file, and returns the channels list.
        
        Returns:
            List[str]: A list of Reddit channel names.
        """
        channels_file_path: str = 'reddit/channels.json'
        if os.path.exists(channels_file_path):
            try:
                with open(channels_file_path, 'r') as file:
                    channels: List[str] = json.load(file)
                    print("Loaded channels from JSON:", channels)
            except json.JSONDecodeError:
                print("Error reading the channels file. It might be corrupted.")
                channels = []
            
            if channels:
                use_channels: str = input("Use these channels? (yes/no): ")
                if use_channels.lower() == 'yes':
                    return channels
        
        csv_input: str = input("Please enter a CSV of Reddit names: ")
        channels: List[str] = [channel.strip() for channel in csv_input.split(',')]
        
        os.makedirs(os.path.dirname(channels_file_path), exist_ok=True)
        
        try:
            with open(channels_file_path, 'w') as file:
                json.dump(channels, file)
            print(f"Saved channels to {channels_file_path}: {channels}")
        except IOError as e:
            print(f"Failed to save channels: {e}")
        
        return channels


    def write_to_json(self, data):
        """
        Writes data to a JSON file named according to the subreddit, date, and mode.

        Parameters:
            subreddit_name (str): The name of the subreddit.
            data (dict): The data to write to the file.
            mode (str): The mode of the subreddit data (e.g., 'hot', 'new', etc.).
        """
        file_path = f'content/${filename}.reddit.json'
        os.makedirs(os.path.dirname(file_path), exist_ok=True)

        try:
            with open(file_path, 'w', encoding='utf-8') as file:
                json.dump(data, file)            
                print(f"Saved Reddit to {file_path}")
        except IOError as e:
            print(f"Failed to save channels: {e}")

        with open(file_path, 'w', encoding='utf-8') as file:
            json.dump(data, file, ensure_ascii=False, indent=4)