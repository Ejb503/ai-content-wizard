import os

HEADERS = {
    "Accept": "application/json",
    "Accept-Encoding": "gzip",
    "X-Subscription-Token": os.getenv("BRAVE_SUMMARIZER")
}

SEARCH_URL = "https://api.search.brave.com/res/v1/web/search"
SUMMARIZER_URL = "https://api.search.brave.com/res/v1/summarizer/search?key={}&entity_info=1"
