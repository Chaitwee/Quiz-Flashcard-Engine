"""Quiz & Flashcard Engine - entry point."""
import logging

from src.utils import setup_logging, get_int, get_text
from src.question_manager import (add_question, view_questions, search_questions,
                                  edit_question, delete_question)
from src.quiz import run_quiz
from src.flashcards import run_flashcards
from src.analytics import show_analytics, show_leaderboard, clear_history


def show_menu(player):
    print("\n===== Quiz & Flashcard Engine =====")
    print("Player:", player)
    print("1.  Take a quiz")
    print("2.  Study with flashcards")
    print("3.  Add a question")
    print("4.  View questions")
    print("5.  Search questions")
    print("6.  Edit a question")
    print("7.  Delete a question")
    print("8.  My analytics")
    print("9.  Leaderboard")
    print("10. Clear my history")
    print("11. Switch player")
    print("12. Exit")


def main():
    setup_logging()
    logging.info("Application started")
    print("Welcome to the Quiz & Flashcard Engine!")
    player = get_text("Enter your name: ")

    while True:
        show_menu(player)
        choice = get_int("Choose an option (1-12): ", 1, 12)
        if choice == 1:
            run_quiz(player)
        elif choice == 2:
            run_flashcards()
        elif choice == 3:
            add_question()
        elif choice == 4:
            view_questions()
        elif choice == 5:
            search_questions()
        elif choice == 6:
            edit_question()
        elif choice == 7:
            delete_question()
        elif choice == 8:
            show_analytics(player)
        elif choice == 9:
            show_leaderboard()
        elif choice == 10:
            clear_history(player)
        elif choice == 11:
            player = get_text("Enter new player name: ")
            logging.info("Switched player to %s", player)
        else:
            print("Goodbye!")
            logging.info("Application closed")
            break


if __name__ == "__main__":
    try:
        main()
    except (KeyboardInterrupt, EOFError):
        print("\nProgram stopped.")
