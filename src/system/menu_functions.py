from linkedin.linkedin_manager import Linkedin
from reddit.reddit_manager import Reddit
from twitter.twitter_manager import Twitter
from arxiv.arxiv_manager import Arxiv

def fetch_data():
    print("Fetching social media topic...")
    submenu_options = [
        "1. Fetch Reddit Posts",
        "2. Fetch arXiv Papers",

    ]
    for option in submenu_options:
        print(option)
    choice = input("Please select an option: ")
    if choice == "1":
        reddit = Reddit()
        channels = Reddit.load_or_create_reddit_channels()
        reddit.fetch_posts(channels, mode='hot')
    elif choice == "2":
        arxiv = Arxiv()
        arxiv.fetch_papers()
    else:
        print("Invalid option selected. Please try again.")

def analyse_data():
    submenu_options = [
        "1. Analyse Reddit Posts",
        "2. Analyse arxiv Posts",
    ]
    print("Analysing social media topic...")
    for option in submenu_options:
        print(option)
    choice = input("Please select an option: ")

    if choice == "1":
        reddit = Reddit()
        reddit.analyse_reddit()

    if choice == "2":
        arxiv = Arxiv()
        arxiv.analyse_paper()

def create_content():
    submenu_options = [
        "1. Create Twitter Post",
        "2. Create LinkedIn Post",
    ]
    print("Analysing social media topic...")
    for option in submenu_options:
        print(option)
    # Prompt user for a choice
    choice = input("Please select an option: ")

    if choice == "1":
        twitter = Twitter()
        twitter.create_tweets()

    if choice == "2":
        linkedin = Linkedin()
        linkedin.create_post()
