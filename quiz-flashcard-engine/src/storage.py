"""Reading and writing the plain text data files.

questions.txt line: question|opt1|opt2|opt3|opt4|answer|category|difficulty
scores.txt line   : date|player|category|score|total|percentage|seconds
"""
import logging
import os

from src.utils import DATA_DIR

QUESTIONS_FILE = os.path.join(DATA_DIR, "questions.txt")
SCORES_FILE = os.path.join(DATA_DIR, "scores.txt")


def read_lines(path):
    """Return all lines of a file. Return an empty list if it cannot be read."""
    if not os.path.exists(path):
        return []
    try:
        with open(path, "r", encoding="utf-8") as file:
            return file.readlines()
    except OSError as error:
        logging.error("Could not read %s: %s", path, error)
        return []


def write_lines(path, lines):
    """Write lines to a file. Return True if it worked."""
    try:
        with open(path, "w", encoding="utf-8") as file:
            for line in lines:
                file.write(line + "\n")
        return True
    except OSError as error:
        logging.error("Could not write %s: %s", path, error)
        return False


def parse_question_line(line):
    """Turn one text line into a question dictionary (None if the line is bad)."""
    parts = line.strip().split("|")
    if len(parts) != 8:
        return None
    try:
        answer = int(parts[5])
    except ValueError:
        return None
    return {
        "question": parts[0],
        "options": parts[1:5],
        "answer": answer,
        "category": parts[6],
        "difficulty": parts[7],
    }


def question_to_line(q):
    parts = [q["question"]] + q["options"]
    parts = parts + [str(q["answer"]), q["category"], q["difficulty"]]
    return "|".join(parts)


def parse_score_line(line):
    """Turn one text line into a score dictionary (None if the line is bad)."""
    parts = line.strip().split("|")
    if len(parts) != 7:
        return None
    try:
        score = int(parts[3])
        total = int(parts[4])
        percentage = float(parts[5])
        seconds = int(parts[6])
    except ValueError:
        return None
    return {
        "date": parts[0],
        "player": parts[1],
        "category": parts[2],
        "score": score,
        "total": total,
        "percentage": percentage,
        "seconds": seconds,
    }


def score_to_line(s):
    parts = [s["date"], s["player"], s["category"], str(s["score"]),
             str(s["total"]), str(s["percentage"]), str(s["seconds"])]
    return "|".join(parts)


def load_questions():
    questions = []
    for line in read_lines(QUESTIONS_FILE):
        if line.strip() == "":
            continue
        question = parse_question_line(line)
        if question is None:
            logging.warning("Skipped bad question line: %s", line.strip())
        else:
            questions.append(question)
    return questions


def save_questions(questions):
    lines = [question_to_line(q) for q in questions]
    return write_lines(QUESTIONS_FILE, lines)


def load_scores():
    scores = []
    for line in read_lines(SCORES_FILE):
        if line.strip() == "":
            continue
        score = parse_score_line(line)
        if score is None:
            logging.warning("Skipped bad score line: %s", line.strip())
        else:
            scores.append(score)
    return scores


def save_scores(scores):
    lines = [score_to_line(s) for s in scores]
    return write_lines(SCORES_FILE, lines)
