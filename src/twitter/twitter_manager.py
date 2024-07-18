import json
import logging
from api.claude import ClaudeChat
from api.fetch_prompt import PromptFetcher
from research.research_manager import research_post
from system.utils import select_content_source, select_post_from_list
from twitter.twitter_config import GENERATE_TWEETS_PROMPT

class Twitter:
    def __init__(self):
        logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

    def create_tweets(self):
        selected_file  = select_content_source('analysis')
        with open(selected_file, 'r', encoding='utf-8') as file:
            analysis = json.load(file)

        topic_source = select_post_from_list(analysis)
        print(f"Selected topic source: {topic_source}")

        filename = input("Enter the filename to save the research: ")
        research = research_post(filename, topic_source['search_query'])

        post_data = {
            "topic_source": topic_source,
            "research": research
        }

        system_instruction, user_instruction, tools = PromptFetcher.fetch_prompt(GENERATE_TWEETS_PROMPT, json.dumps(post_data))
        file_path = f'content/{filename}.twitter.json'
        result = ClaudeChat.send_message(file_path, system_instruction, user_instruction, tools)
        self.convert_to_post(result)

    def convert_to_post(self, content):
        if isinstance(content, str):
            content = json.loads(content)
            
        tweets = content["content"][0]["input"]["tweets"]

        # Print each tweet
        for tweet in tweets:
            print(tweet)


