import glob
import os

from colorama import Style
from pygments import highlight
import pygments
from pygments.lexers import get_lexer_by_name
from pygments.formatters import TerminalFormatter

from system.config import BLUE

def print_colored(text, color):
    print(f"{color}{text}{Style.RESET_ALL}")

def print_code(code, language):
    try:
        lexer = get_lexer_by_name(language, stripall=True)
        formatted_code = highlight(code, lexer, TerminalFormatter())
        print(formatted_code)
    except pygments.util.ClassNotFound:
        print_colored(f"Code (language: {language}):\n{code}", BLUE)


def select_content_source(required_string):
    content_dir = './content'
    json_files = glob.glob(os.path.join(content_dir, '*.json'))
    
    json_files = [file for file in json_files if required_string in os.path.basename(file)]
    
    if not json_files:
        print("No JSON files found in the 'content' folder.")
        return None
    
    for index, file in enumerate(json_files, start=1):
        print(f"{index}. {os.path.basename(file)}")
    
    while True:
        try:
            choice = int(input("Select the file number you want to use: "))
            if 1 <= choice <= len(json_files):
                selected_file = json_files[choice - 1]
                print(f"You selected: {selected_file}")
                return selected_file
            else:
                print("Invalid selection. Please select a number from the list.")
        except ValueError:
            print("Please enter a valid number.")

def select_post_from_list(content):
    posts = content['content'][0]['input']['posts']

    for index, post in enumerate(posts, start=1):
        print(f"{index}. {post['title']}")
        print(f"{post['relevance']}")

    while True:
        try:
            choice = int(input("Select the post number you want to view: "))
            if 1 <= choice <= len(posts):
                selected_post = posts[choice - 1]
                return selected_post
            else:
                print("Invalid selection. Please select a number from the list.")
        except ValueError:
            print("Please enter a valid number.")

def select_arxiv_post_from_list(content):

    for index, post in enumerate(content, start=1):
        print(f"{index}. {post['title']}")

    while True:
        try:
            choice = int(input("Select the post number you want to view: "))
            if 1 <= choice <= len(content):
                selected_post = content[choice - 1]
                return selected_post
            else:
                print("Invalid selection. Please select a number from the list.")
        except ValueError:
            print("Please enter a valid number.")