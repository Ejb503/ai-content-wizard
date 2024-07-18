import os
from dotenv import load_dotenv
from colorama import init
from system import menu_functions
from system.config import BLUE, RED, main_options
from system.utils import print_colored

load_dotenv()

def create_folder(path):
    try:
        os.makedirs(path, exist_ok=True)
        return f"Folder created: {path}"
    except Exception as e:
        return f"Error creating folder: {str(e)}"

def get_user_choice(options):
    while True:
        for i, option in enumerate(options, start=1):
            print(f"{i}. {option}")
        user_input = input("\nYour choice: ")
        if user_input.lower() == 'exit':
            return 'exit'
        try:
            choice = int(user_input) - 1
            if 0 <= choice < len(options):
                return options[choice]
            else:
                raise ValueError
        except ValueError:
            print_colored("Invalid selection. Please try again.", RED)

def main():
    init()
    while True:
        print_colored("Welcome to the Social Media Content generator!", BLUE)
        selected_option = get_user_choice(main_options)
        if selected_option == 'exit':
            print_colored("Thank you for using the Social Media Content generator. Goodbye!", BLUE)
            break
        option_function = getattr(menu_functions, selected_option, None)
        if option_function:
            option_function()
        else:
            print_colored("Option not implemented.", RED)

if __name__ == "__main__":
    main()