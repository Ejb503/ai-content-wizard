import requests
import xml.etree.ElementTree as ET
import json
from bs4 import BeautifulSoup

from system.utils import select_arxiv_post_from_list, select_content_source

class Arxiv:
    def __init__(self):
        self.base_url = "https://export.arxiv.org/api/query?search_query=cat:cs.AI&start=0&max_results=100&sortBy=submittedDate&sortOrder=descending"

    def fetch_papers(self):
        response = requests.get(self.base_url)
        if response.status_code != 200:
            return "Failed to fetch the RSS feed"
        
        root = ET.fromstring(response.content)
        entries = []
        
        for entry in root.findall('./{http://www.w3.org/2005/Atom}entry'):
            link = entry.find('{http://www.w3.org/2005/Atom}link').attrib['href']
            link = link.replace('abs', 'html')  # Replace 'abs' with 'html' in the link
            entry_data = {
                'title': entry.find('{http://www.w3.org/2005/Atom}title').text,
                'summary': entry.find('{http://www.w3.org/2005/Atom}summary').text,
                'published': entry.find('{http://www.w3.org/2005/Atom}published').text,
                'link': link
            }
            entries.append(entry_data)
        
        try:
            with open('content/arxiv.source.json', 'w', encoding='utf-8') as file:
                json.dump(entries, file)            
                print(f"Saved Reddit to {'content/arxiv.source.json'}")
        except Exception as e:
            print(f"Failed to save arxiv Article: {e}")


        return json.dumps(entries, indent=4)

    def analyse_paper(self): 
        content_source  = select_content_source('source')
        with open(content_source, 'r', encoding='utf-8') as file:
            content = json.load(file)
        selected_file  = select_arxiv_post_from_list(content)
        print(selected_file)
        return selected_file
        
    def convert_html_to_json(filename, url):
        response = requests.get(url)
        soup = BeautifulSoup(response.text, "html.parser")
        article = " ".join([element.text for element in soup.find_all(["p", "h1", "h2", "h3"])])
        file_path = f'content/{filename}.arxiv.json'
        try:
            with open(file_path, 'w', encoding='utf-8') as file:
                json.dump(article, file)            
                print(f"Saved Reddit to {file_path}")
        except Exception as e:
            print(f"Failed to save arxiv Article: {e}")



