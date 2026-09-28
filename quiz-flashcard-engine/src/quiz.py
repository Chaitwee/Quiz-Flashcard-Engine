"""Module 2: Quiz mode (scoring, 50-50 lifeline, timer, answer review)."""
import logging
import random
import time
from datetime import datetime

from src import storage
from src.utils import DIFFICULTIES, get_int


def check_answer(question, choice):
    """Return True if the chosen option number is correct."""
    return choice == question["answer"]


def calculate_percentage(score, total):
    if total == 0:
        return 0.0
    return round(score / total * 100, 2)


def get_grade(percentage):
    if percentage >= 80:
        return "Excellent!"
    elif percentage >= 50:
        return "Good effort, keep practising."
    else:
        return "Needs more practice."


def get_categories(questions):
    """Return a list of unique categories."""
    categories = []
    for q in questions:
        if q["category"] not in categories:
            categories.append(q["category"])
    return categories


def filter_questions(questions, category, difficulty):
    """None for category or difficulty means 'all'."""
    result = []
    for q in questions:
        if category is not None and q["category"] != category:
            continue
        if difficulty is not None and q["difficulty"] != difficulty:
            continue
        result.append(q)
    return result


def fifty_fifty(question):
    """Return two option numbers to keep: the right one and one wrong one."""
    wrong = []
    for number in range(1, 5):
        if number != question["answer"]:
            wrong.append(number)
    keep = [question["answer"], random.choice(wrong)]
    keep.sort()
    return keep


def choose_filters(questions):
    """Ask the user for a category and a difficulty."""
    categories = get_categories(questions)
    print("0. All categories")
    for i, cat in enumerate(categories, start=1):
        print(str(i) + ". " + cat)
    choice = get_int("Choose a category: ", 0, len(categories))
    category = None if choice == 0 else categories[choice - 1]

    print("\n0. All difficulties")
    for i, level in enumerate(DIFFICULTIES, start=1):
        print(str(i) + ". " + level)
    level_choice = get_int("Choose a difficulty: ", 0, len(DIFFICULTIES))
    difficulty = None if level_choice == 0 else DIFFICULTIES[level_choice - 1]
    return category, difficulty


def ask_answer(question, lifeline_available):
    """Ask for an answer. Return (answer, lifeline_used_now)."""
    if lifeline_available:
        prompt = "Your answer (1-4, or 5 for the 50-50 lifeline): "
        high = 5
    else:
        prompt = "Your answer (1-4): "
        high = 4

    answer = get_int(prompt, 1, high)
    if answer != 5:
        return answer, False

    keep = fifty_fifty(question)
    print("50-50 used! Remaining options:")
    for number in keep:
        print("   " + str(number) + ") " + question["options"][number - 1])
    answer = get_int("Your answer: ", 1, 4)
    while answer not in keep:
        print("Choose option", keep[0], "or", keep[1])
        answer = get_int("Your answer: ", 1, 4)
    return answer, True


def show_review(wrong):
    """Show every question the user got wrong."""
    print("\n--- Review of Wrong Answers ---")
    if len(wrong) == 0:
        print("Perfect score! Nothing to review.")
        return
    for q, chosen in wrong:
        print("\nQ:", q["question"])
        print("  Your answer   :", q["options"][chosen - 1])
        print("  Correct answer:", q["options"][q["answer"] - 1])


def run_quiz(player):
    questions = storage.load_questions()
    if len(questions) == 0:
        print("No questions available. Add some first.")
        return

    print("\n--- Quiz Mode ---")
    category, difficulty = choose_filters(questions)
    available = filter_questions(questions, category, difficulty)
    if len(available) == 0:
        print("No questions match that choice.")
        return

    count = get_int("How many questions (1-" + str(len(available)) + ")? ", 1, len(available))
    selected = random.sample(available, count)

    score = 0
    wrong = []
    lifeline_available = True
    start = time.time()

    for number, q in enumerate(selected, start=1):
        print("\nQ" + str(number) + ". " + q["question"])
        for i, option in enumerate(q["options"], start=1):
            print("   " + str(i) + ") " + option)
        answer, used_now = ask_answer(q, lifeline_available)
        if used_now:
            lifeline_available = False
        if check_answer(q, answer):
            print("Correct!")
            score += 1
        else:
            print("Wrong.")
            wrong.append((q, answer))

    seconds = int(time.time() - start)
    percentage = calculate_percentage(score, count)
    print("\n" + player + ", you scored", score, "out of", count, "(" + str(percentage) + "%)")
    print("Time taken:", seconds, "seconds")
    print(get_grade(percentage))
    show_review(wrong)

    scores = storage.load_scores()
    scores.append({
        "date": datetime.now().strftime("%Y-%m-%d %H:%M"),
        "player": player,
        "category": category if category else "All",
        "score": score,
        "total": count,
        "percentage": percentage,
        "seconds": seconds,
    })
    storage.save_scores(scores)
    logging.info("%s finished quiz: %s/%s in %s seconds", player, score, count, seconds)
