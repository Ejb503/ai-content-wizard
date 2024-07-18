# Functions corresponding to each menu option
from linkedin.linkedin_manager import Linkedin
from reddit.reddit_manager import Reddit
from twitter.twitter_manager import Twitter

def fetch_topic():
    print("Fetching social media topic...")
    submenu_options = [
        "1. Fetch Reddit Posts",
    ]
    for option in submenu_options:
        print(option)
    choice = input("Please select an option: ")
    if choice == "1":
        reddit = Reddit()
        print("Fetching trending topics...")
        channels = Reddit.load_or_create_reddit_channels()
        print("Fetching Reddit posts for channels:", channels)
        reddit.fetch_posts(channels, mode='hot')
    elif choice == "2":
        print("Fetching topics based on user interests...")
    elif choice == "3":
        print("Please enter your custom topic:")
        custom_topic = input()
        print(f"Fetching information for {custom_topic}...")
    elif choice == "4":
        print("Returning to main menu...")
    else:
        print("Invalid option selected. Please try again.")

def analyse_topic():
    submenu_options = [
        "1. Analyse Reddit Posts",
        "2. Analyse arxiv Posts",
    ]
    print("Analysing social media topic...")
    for option in submenu_options:
        print(option)
    # Prompt user for a choice
    choice = input("Please select an option: ")

    if choice == "1":
        reddit = Reddit()
        reddit.analyse_reddit()

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
