import json
import logging
from api.claude import ClaudeChat
from api.fetch_prompt import PromptFetcher
from research.research_manager import research_post
from linkedin.linkedin_config import GENERATE_LINKEDIN_PROMPT
from system.utils import select_content_source, select_post_from_list

class Linkedin:
    def __init__(self):
        logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

    def create_post(self):
        selected_file  = select_content_source('analysis')
        with open(selected_file, 'r', encoding='utf-8') as file:
            reddit_content = json.load(file)

        topic_source = select_post_from_list(reddit_content)
        print(f"Selected topic source: {topic_source}")

        filename = input("Enter the filename to save the research: ")
        research = research_post(filename, topic_source['search_query'])

        post_data = {
            "topic_source": topic_source,
            "research": research
        }

        system_instruction, user_instruction, tools = PromptFetcher.fetch_prompt(GENERATE_LINKEDIN_PROMPT, json.dumps(post_data))
        file_path = f'content/{filename}.linkedin.json'
        result = ClaudeChat.send_message(file_path, system_instruction, user_instruction, tools)
        self.convert_to_post(result)
        

    def convert_to_post(self, content):
        if isinstance(content, str):
            content = json.loads(content)
        content = content["content"][0]["input"]["linkedin_post"]

        post_text = f"{content['headline']}\n\n" \
                    f"{content['paragraph1']}\n\n" \
                    f"{content['paragraph2']}\n\n" \
                    f"{content['paragraph3']}\n\n" \
                    f"{content['paragraph4']}\n\n" \
                    f"{' '.join(content['hashtags'])}\n\n"

        print(post_text)
        return post_text