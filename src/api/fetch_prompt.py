import requests
import json
import logging

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

class PromptFetcher:
    def fetch_prompt(prompt_uuid, content, api_key='22bb58e99be3b1c49e6af5a2c5c524b3'):
        api_link = f'http://localhost/api/prompt/{prompt_uuid}'

        json_payload = {
            "content": content
        }

        headers = {
            'Accept': 'application/json',
            'Content-Type': 'application/json',
            'api-key': api_key
        }

        try:
            print(json_payload)
            response = requests.post(api_link, headers=headers, json=json_payload)
            # Check if the response status code is 200 (OK)
            if response.status_code != 200:
                logging.error(f'Failed to fetch prompt: {response.status_code} - {response.text}')
                return None

            try:
                response_json = response.json()
            except json.JSONDecodeError:
                logging.error('Failed to decode JSON from response')
                return None

            with open('prompt.json', 'w') as file:
                json.dump(response_json, file, indent=4)

            system_instruction = response_json.get('system_instruction', '')
            user_instruction = response_json.get('user_instruction', '')
            tools = response_json.get('tools', '')

            logging.info(f'Prompt {prompt_uuid} fetched successfully')
            return system_instruction, user_instruction, tools
        except requests.exceptions.RequestException as e:
            logging.error(f'Error fetching prompt: {e}')
            return None