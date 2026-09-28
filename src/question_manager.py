"""Module 1: Question bank management (add, view, search, edit, delete)."""
import logging

from src import storage
from src.utils import DIFFICULTIES, get_int, get_text


def create_question(text, options, answer, category, difficulty):
    """Build a question dictionary after checking the values."""
    if text.strip() == "":
        raise ValueError("Question text cannot be empty.")
    if len(options) != 4:
        raise ValueError("A question must have exactly 4 options.")
    if answer < 1 or answer > 4:
        raise ValueError("Answer must be between 1 and 4.")
    if category.strip() == "":
        raise ValueError("Category cannot be empty.")
    if difficulty not in DIFFICULTIES:
        raise ValueError("Difficulty must be Easy, Medium or Hard.")
    for item in [text, category] + options:
        if "|" in item:
            raise ValueError("The '|' character is not allowed.")
    return {
        "question": text.strip(),
        "options": options,
        "answer": answer,
        "category": category.strip(),
        "difficulty": difficulty,
    }


def find_questions(questions, keyword):
    """Return questions whose text or category contains the keyword."""
    keyword = keyword.lower()
    found = []
    for q in questions:
        if keyword in q["question"].lower() or keyword in q["category"].lower():
            found.append(q)
    return found


def ask_difficulty():
    for i, level in enumerate(DIFFICULTIES, start=1):
        print(str(i) + ". " + level)
    choice = get_int("Choose difficulty (1-3): ", 1, 3)
    return DIFFICULTIES[choice - 1]


def print_question_line(number, q):
    print(str(number) + ". [" + q["category"] + " | " + q["difficulty"] + "] " + q["question"])


def add_question():
    print("\n--- Add a New Question ---")
    text = get_text("Question: ")
    options = []
    for i in range(1, 5):
        options.append(get_text("Option " + str(i) + ": "))
    answer = get_int("Correct option number (1-4): ", 1, 4)
    category = get_text("Category: ")
    difficulty = ask_difficulty()

    try:
        question = create_question(text, options, answer, category, difficulty)
    except ValueError as error:
        print("Error:", error)
        return

    questions = storage.load_questions()
    questions.append(question)
    if storage.save_questions(questions):
        logging.info("Added question: %s", text)
        print("Question added.")
    else:
        print("Could not save the question.")


def view_questions():
    questions = storage.load_questions()
    print("\n--- Question Bank (" + str(len(questions)) + " questions) ---")
    if len(questions) == 0:
        print("No questions yet.")
        return
    for number, q in enumerate(questions, start=1):
        print_question_line(number, q)


def search_questions():
    print("\n--- Search Questions ---")
    keyword = get_text("Enter a keyword: ")
    found = find_questions(storage.load_questions(), keyword)
    if len(found) == 0:
        print("No matching questions.")
        return
    print(len(found), "match(es) found:")
    for number, q in enumerate(found, start=1):
        print_question_line(number, q)


def edit_question():
    questions = storage.load_questions()
    if len(questions) == 0:
        print("No questions to edit.")
        return
    view_questions()
    number = get_int("Number to edit (0 to cancel): ", 0, len(questions))
    if number == 0:
        return
    q = questions[number - 1]

    print("\nWhat do you want to change?")
    print("1. Question text")
    print("2. Options")
    print("3. Correct answer")
    print("4. Category")
    print("5. Difficulty")
    field = get_int("Choose (1-5): ", 1, 5)

    if field == 1:
        q["question"] = get_text("New question text: ")
    elif field == 2:
        for i in range(4):
            q["options"][i] = get_text("New option " + str(i + 1) + ": ")
    elif field == 3:
        q["answer"] = get_int("New correct option number (1-4): ", 1, 4)
    elif field == 4:
        q["category"] = get_text("New category: ")
    else:
        q["difficulty"] = ask_difficulty()

    if storage.save_questions(questions):
        logging.info("Edited question number %s", number)
        print("Question updated.")


def delete_question():
    questions = storage.load_questions()
    if len(questions) == 0:
        print("No questions to delete.")
        return
    view_questions()
    number = get_int("Number to delete (0 to cancel): ", 0, len(questions))
    if number == 0:
        return
    removed = questions.pop(number - 1)
    if storage.save_questions(questions):
        logging.info("Deleted question: %s", removed["question"])
        print("Question deleted.")
