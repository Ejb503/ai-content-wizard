import requests
import xml.etree.ElementTree as ET
import json

class ArxivFetcher:
    def __init__(self):
        self.base_url = "https://export.arxiv.org/api/query?search_query=cat:cs.AI&start=0&max_results=100&sortBy=submittedDate&sortOrder=descending"

    def fetch_and_convert_rss_to_json(self):
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
        
        return json.dumps(entries, indent=4)

    def retrieve_ai(self):
        return self.fetch_and_convert_rss_to_json()

