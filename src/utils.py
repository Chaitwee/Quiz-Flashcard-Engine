"""Helper functions: paths, logging and safe user input."""
import logging
import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_DIR = os.path.join(BASE_DIR, "data")
LOG_FILE = os.path.join(BASE_DIR, "app.log")

DIFFICULTIES = ["Easy", "Medium", "Hard"]


def setup_logging():
    """Send log messages to app.log."""
    logging.basicConfig(
        filename=LOG_FILE,
        level=logging.INFO,
        format="%(asctime)s - %(levelname)s - %(message)s",
    )


def get_int(prompt, low, high):
    """Keep asking until the user types a whole number between low and high."""
    while True:
        value = input(prompt).strip()
        try:
            number = int(value)
        except ValueError:
            print("Please enter a number.")
            continue
        if number < low or number > high:
            print("Please enter a number between", low, "and", high)
            continue
        return number


def get_text(prompt):
    """Keep asking until the user types non-empty text without the | symbol."""
    while True:
        value = input(prompt).strip()
        if value == "":
            print("Input cannot be empty.")
        elif "|" in value:
            print("The '|' character is not allowed.")
        else:
            return value


def get_yes_no(prompt):
    """Return True for y and False for n."""
    while True:
        value = input(prompt).strip().lower()
        if value == "y":
            return True
        if value == "n":
            return False
        print("Please type y or n.")
