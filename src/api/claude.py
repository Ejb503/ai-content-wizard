import os
import json
import logging
from anthropic import Anthropic

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

class ClaudeChat:
    def send_message(file_path, system_message, user_message, tools):
        try:
            api_key = os.getenv("CLAUDE_API_KEY")
            if not api_key:
                logging.error("CLAUDE_API_KEY is not set.")
                return None

            print(f"Claude beginning analysis {file_path}.")  

            client = Anthropic(api_key=api_key)

            response = client.messages.create(
                model="claude-3-5-sonnet-20240620",
                max_tokens=4096,
                system=system_message,
                messages=[{"role": "user", "content": user_message}],
                tools=tools,
                tool_choice={"type": "tool", "name": tools[0].get("name", "")}
            )
            response_data = response.json()

            with open(file_path, 'w') as file:
                json.dump(json.loads(response_data), file, indent=4)
            logging.info(f"Response saved to {file_path}")
            return response_data
        
        except Exception as e:
            logging.error(f"An error occurred: {e}")
            return None