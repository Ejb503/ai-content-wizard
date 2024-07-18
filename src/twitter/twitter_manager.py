import json
import logging
import os
import glob
from api.claude import ClaudeChat
from api.fetch_prompt import PromptFetcher
from research.research_manager import research_post
from twitter.twitter_config import GENERATE_TWEETS_PROMPT

class Twitter:
    def __init__(self):
        logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

    def create_tweets(self):
        selected_file  = self.select_content_source()
        with open(selected_file, 'r', encoding='utf-8') as file:
            reddit_content = json.load(file)

        topic_source = self.select_post_from_list(reddit_content)
        print(f"Selected topic source: {topic_source}")

        filename = input("Enter the filename to save the research: ")
        research = research_post(filename, topic_source['search_query'])

        post_data = {
            "topic_source": topic_source,
            "research": research
        }
        system_instruction, user_instruction, tools = PromptFetcher.fetch_prompt(GENERATE_TWEETS_PROMPT, json.dumps(post_data))
        file_path = f'content/{filename}.twitter.json'
        ClaudeChat.send_message(file_path, system_instruction, user_instruction, tools)

    def select_content_source(self):
        content_dir = './content'
        json_files = glob.glob(os.path.join(content_dir, '*.json'))
        
        if not json_files:
            print("No JSON files found in the 'content' folder.")
            return None
        
        for index, file in enumerate(json_files, start=1):
            print(f"{index}. {os.path.basename(file)}")
        
        while True:
            try:
                choice = int(input("Select the file number you want to use: "))
                if 1 <= choice <= len(json_files):
                    selected_file = json_files[choice - 1]
                    print(f"You selected: {selected_file}")
                    return selected_file
                else:
                    print("Invalid selection. Please select a number from the list.")
            except ValueError:
                print("Please enter a valid number.")

    def select_post_from_list(self, content):
        # Assuming 'content' is the parsed JSON object provided in the question
        # Extract the list of posts from the nested structure
        posts = content['content'][0]['input']['posts']

        # Display each post's title with an index
        for index, post in enumerate(posts, start=1):
            print(f"{index}. {post['title']}")
            print(f"{post['relevance']}")

        # Prompt the user to select a post4
        while True:
            try:
                choice = int(input("Select the post number you want to view: "))
                # Validate the user's choice
                if 1 <= choice <= len(posts):
                    selected_post = posts[choice - 1]
                    return selected_post
                else:
                    print("Invalid selection. Please select a number from the list.")
            except ValueError:
                print("Please enter a valid number.")
