"""Module 3: Flashcard study mode with repeat rounds for missed cards."""
import logging
import random

from src import storage
from src.quiz import choose_filters, filter_questions
from src.utils import get_yes_no


def get_correct_answer_text(question):
    return question["options"][question["answer"] - 1]


def run_flashcards():
    questions = storage.load_questions()
    if len(questions) == 0:
        print("No questions available. Add some first.")
        return

    print("\n--- Flashcard Mode ---")
    category, difficulty = choose_filters(questions)
    cards = filter_questions(questions, category, difficulty)[:]
    if len(cards) == 0:
        print("No questions match that choice.")
        return
    random.shuffle(cards)

    round_number = 1
    while len(cards) > 0:
        print("\n=== Round " + str(round_number) + " (" + str(len(cards)) + " cards) ===")
        missed = []
        for number, card in enumerate(cards, start=1):
            print("\nCard " + str(number) + " of " + str(len(cards)))
            print("Q:", card["question"])
            input("Press Enter to reveal the answer...")
            print("A:", get_correct_answer_text(card))
            if not get_yes_no("Did you know it? (y/n): "):
                missed.append(card)

        known = len(cards) - len(missed)
        print("\nYou knew", known, "of", len(cards), "cards.")
        logging.info("Flashcard round %s: %s/%s known", round_number, known, len(cards))

        if len(missed) == 0:
            print("Great! You know all the cards.")
            break
        if not get_yes_no("Review the " + str(len(missed)) + " missed cards again? (y/n): "):
            break
        cards = missed
        round_number += 1
