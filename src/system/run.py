import logging
import os
from typing import List, Tuple, Dict, Any
from api.claude import ClaudeChat
from api.fetch_prompt import PromptFetcher
from reddit.reddit_manager import RedditFetcher
import json
import uuid

# Initialize logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Configuration
REDDIT_USER_AGENT ='myRedditApp/1.0 by /u/ejb503'
ANALYSE_REDDIT_PROMPT ='10d68722-6484-4ab8-a123-8a095bafa933'
GENERATE_TWEETS_PROMPT = 'd2c034b8-cf6f-46f2-894b-219a2629a9c6'
GENERATE_LINKEDIN_PROMPT = 'beb2445a-dd53-4ef2-a895-ea3eda26cba6'
SUBREDDIT_NAMES = ['ArtificialInteligence', 'generativeAI', 'LocalLlama', 'OpenAI', 'MachineLearning']

def fetch_and_analyze_reddit_posts(subreddit_names: List[str], user_agent: str) -> Tuple[str, str, List[Dict[str, Any]]]:
    try:
        reddit_fetcher = RedditFetcher(subreddit_names, user_agent=user_agent)
        content = reddit_fetcher.fetch_posts(mode='hot')
        return content
    except Exception as e:
        logging.error(f"Failed to fetch and analyze Reddit posts: {e}")
        raise



def generate_tweets():
    research_folder = 'focus'  # Adjust the path as necessary
    for file_name in os.listdir(research_folder):
        if file_name.endswith('.json'):
            full_path = os.path.join(research_folder, file_name)
            with open(full_path, 'r') as file:
                data = json.load(file)
                id, system_instruction, user_instruction, tools = fetch_prompt(GENERATE_TWEETS_PROMPT, json.dumps(data))
                print(id)
                print(system_instruction)
                print(user_instruction)
                print(tools)
                tweets = generate_and_send_message(id, system_instruction, user_instruction, tools)
                tweet_id = uuid.uuid4()
                # # Save result to a file named research_id.json
                with open(f'tweets/{tweet_id}.json', 'w') as file:
                    json.dump(json.loads(tweets), file, indent=4)


def generate_linkedin():
    research_folder = 'research'  # Adjust the path as necessary
    for file_name in os.listdir(research_folder):
        if file_name.endswith('.json'):
            full_path = os.path.join(research_folder, file_name)
            with open(full_path, 'r') as file:
                data = json.load(file)
                id, system_instruction, user_instruction, tools = fetch_prompt(GENERATE_LINKEDIN_PROMPT, json.dumps(data))
                posts = generate_and_send_message(id, system_instruction, user_instruction, tools)
                post_id = uuid.uuid4()
                # # Save result to a file named research_id.json
                with open(f'linkedin/{post_id}.json', 'w') as file:
                    json.dump(json.loads(posts), file, indent=4)

def main():
    try:
        generate_tweets()
        content = fetch_and_analyze_reddit_posts(SUBREDDIT_NAMES, REDDIT_USER_AGENT)
        id, system_instruction, user_instruction, tools = fetch_prompt(ANALYSE_REDDIT_PROMPT, content)
        reddit_analysis = generate_and_send_message(id, system_instruction, user_instruction, tools)
        def load_claude_response(file_path: str) -> dict:
            try:
                with open(file_path, 'r') as file:
                    data = json.load(file)
                return data
            except Exception as e:
                logging.error(f"Failed to load Claude response from {file_path}: {e}")
                raise

    #     # Example usage
    #     file_path = 'claude_response_10d68722-6484-4ab8-a123-8a095bafa933.json'
    #     claude_response = json.loads(load_claude_response(file_path))
    #     print(json.dumps(claude_response))
    #     contents = claude_response.get('content', [])
    #     for content in contents:
    #         posts = content.get('input', {}).get('posts', [])
    #         for post in posts:
    #             id = uuid.uuid4()
    #             print('Post:', post)
    #             research = research_post(post.get('title'), id)
    #             # print(tweets)
    except Exception as e:
        logging.error(f"An error occurred: {e}")

if __name__ == "__main__":
    main()