import uuid
from arxiv.fetch_arxiv import ArxivFetcher
from api.fetch_prompt import PromptFetcher
import json
import requests
import re
from bs4 import BeautifulSoup

from system.run import generate_and_send_message

CHOOSE_ARXIV_PAPER = '10d68722-6484-4ab8-a123-8a095bafa933'
ANALYSE_ARXIV_PAPER = '9ba7522f-a658-4af4-a2fc-53772e58bd1b'

# fetcher = ArxivFetcher()
# ai_papers = fetcher.retrieve_ai()
# print(ai_papers)
# id, system_instruction, user_instruction, tools = PromptFetcher().fetch_prompt(ANALYSE_ARXIV_PAPER, json.dumps(ai_papers))
# print(id, system_instruction, user_instruction, tools)
# posts = generate_and_send_message(id, system_instruction, user_instruction, tools)
# post_id = uuid.uuid4()
# with open(f'arxiv/{post_id}.json', 'w') as file:
#     json.dump(json.loads(posts), file, indent=4)

url = "http://arxiv.org/html/2407.11300v1"
response = requests.get(url)
soup = BeautifulSoup(response.text, "html.parser")
article = " ".join([element.text for element in soup.find_all(["p", "h1", "h2", "h3"])])
id, system_instruction, user_instruction, tools = PromptFetcher().fetch_prompt(ANALYSE_ARXIV_PAPER, article)
id = uuid.uuid4()
posts = generate_and_send_message(id, system_instruction, user_instruction, tools)
