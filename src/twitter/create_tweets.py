
import json
import os
import uuid
from system.run import fetch_prompt, generate_and_send_message

GENERATE_TWEETS_PROMPT = 'd2c034b8-cf6f-46f2-894b-219a2629a9c6'

def create_tweets():
    research_folder = 'focus'  # Adjust the path as necessary
    for file_name in os.listdir(research_folder):
        if file_name.endswith('.json'):
            full_path = os.path.join(research_folder, file_name)
            with open(full_path, 'r') as file:
                data = json.load(file)
                id, system_instruction, user_instruction, tools = fetch_prompt(GENERATE_TWEETS_PROMPT, json.dumps(data))
                tweets = generate_and_send_message(id, system_instruction, user_instruction, tools)
                tweet_id = uuid.uuid4()
                with open(f'tweets/{tweet_id}.json', 'w') as file:
                    json.dump(json.loads(tweets), file, indent=4)

create_tweets()