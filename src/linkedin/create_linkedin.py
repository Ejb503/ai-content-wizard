import json
import os
import uuid
from system.run import fetch_prompt, generate_and_send_message

GENERATE_LINKEDIN_PROMPT = 'beb2445a-dd53-4ef2-a895-ea3eda26cba6'

def generate_linkedin():
    research_folder = 'focus'  # Adjust the path as necessary
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

generate_linkedin()