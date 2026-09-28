# Quiz & Flashcard Engine

A command-line Python application for self-testing and revision using multiple-choice quizzes and flashcards.

## Overview
Users keep a question bank in a plain text file, take timed quizzes filtered by category and difficulty, revise with flashcards, and track their progress. See `statement.md` for the full problem statement.

## Features
- **Players:** enter your name; scores are saved per player and you can switch player at any time
- **Question management:** add, view, search, edit and delete questions (with category and Easy/Medium/Hard difficulty)
- **Quiz mode:** filter by category and difficulty, choose how many questions, use a one-time 50-50 lifeline, see your time, grade and a review of wrong answers
- **Flashcard mode:** reveal answers, mark known/not known, and repeat missed cards in extra rounds
- **Analytics:** attempts, average/best/worst score, average time, per-category averages, last 5 attempts
- **Leaderboard:** top 5 scores across all players (ties broken by time)
- **Clear history:** delete your own attempts
- Input validation, error handling and logging to `app.log`

## Technologies Used
- Python 3.8+ (standard library only: `os`, `random`, `time`, `logging`, `datetime`, `unittest`)
- Plain text files for storage
- Git and GitHub for version control

## Project Structure
```
quiz-flashcard-engine/
├── main.py                  # entry point and menu
├── src/
│   ├── utils.py             # paths, logging, safe input
│   ├── storage.py           # text file read/write and parsing
│   ├── question_manager.py  # add / view / search / edit / delete questions
│   ├── quiz.py              # quiz mode, lifeline, timer, review
│   ├── flashcards.py        # flashcard mode
│   └── analytics.py         # statistics, leaderboard, clear history
├── data/
│   ├── questions.txt        # question bank (17 sample questions)
│   └── scores.txt           # quiz history
├── tests/test_engine.py     # unit tests
└── statement.md
```

## Data File Formats
`data/questions.txt` (one question per line, fields separated by `|`):
```
question|option1|option2|option3|option4|correct_option_number|category|difficulty
```
`data/scores.txt`:
```
date|player|category|score|total|percentage|seconds
```

## Installation and Setup
1. Install Python 3.8 or newer from https://www.python.org/downloads/ and check it with:
   ```
   python --version
   ```
2. Download the project:
   ```
   git clone https://github.com/<your-username>/<repo-name>.git
   cd <repo-name>
   ```
3. No extra libraries are needed, so there is no `pip install` step and no configuration.

## How to Run
From the project root folder:
```
python main.py
```
(Use `python3 main.py` on Linux/macOS.) You can also open `main.py` in IDLE and press F5.

## How to Run the Tests
From the project root folder:
```
python -m unittest discover -s tests -t .
```
All 19 tests should pass.

## Non-Functional Requirements
- **Error handling:** invalid input is re-prompted; missing or corrupt data lines are skipped safely
- **Reliability:** the program does not crash on bad input; Ctrl+C exits cleanly
- **Logging:** key events, warnings and errors are written to `app.log`
- **Usability:** numbered menus, clear messages, instant feedback and a grade after each quiz
- **Maintainability:** each feature lives in its own module with small, testable functions

## Screenshots
Add screenshots of the menu, a quiz run and the analytics screen here.

## Future Enhancements
Import/export of question sets, spaced-repetition scheduling, per-question time limits.
