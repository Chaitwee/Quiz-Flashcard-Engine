import unittest

from src.question_manager import create_question, find_questions
from src.quiz import (check_answer, calculate_percentage, get_grade, get_categories,
                      filter_questions, fifty_fifty)
from src.analytics import compute_stats, top_scores, get_player_scores
from src.storage import (parse_question_line, question_to_line,
                         parse_score_line, score_to_line)

SAMPLE = [
    {"question": "Q1", "options": ["a", "b", "c", "d"], "answer": 2,
     "category": "Python", "difficulty": "Easy"},
    {"question": "Q2 loops", "options": ["a", "b", "c", "d"], "answer": 1,
     "category": "Maths", "difficulty": "Hard"},
]


class TestQuestionManager(unittest.TestCase):
    def test_valid_question(self):
        q = create_question("What?", ["a", "b", "c", "d"], 3, "Python", "Easy")
        self.assertEqual(q["answer"], 3)

    def test_empty_text(self):
        with self.assertRaises(ValueError):
            create_question("  ", ["a", "b", "c", "d"], 1, "Python", "Easy")

    def test_wrong_option_count(self):
        with self.assertRaises(ValueError):
            create_question("What?", ["a", "b"], 1, "Python", "Easy")

    def test_bad_answer_number(self):
        with self.assertRaises(ValueError):
            create_question("What?", ["a", "b", "c", "d"], 5, "Python", "Easy")

    def test_bad_difficulty(self):
        with self.assertRaises(ValueError):
            create_question("What?", ["a", "b", "c", "d"], 1, "Python", "Impossible")

    def test_pipe_rejected(self):
        with self.assertRaises(ValueError):
            create_question("A|B?", ["a", "b", "c", "d"], 1, "Python", "Easy")

    def test_search(self):
        self.assertEqual(len(find_questions(SAMPLE, "loops")), 1)
        self.assertEqual(len(find_questions(SAMPLE, "python")), 1)
        self.assertEqual(len(find_questions(SAMPLE, "zzz")), 0)


class TestQuiz(unittest.TestCase):
    def test_check_answer(self):
        self.assertTrue(check_answer(SAMPLE[0], 2))
        self.assertFalse(check_answer(SAMPLE[0], 1))

    def test_percentage(self):
        self.assertEqual(calculate_percentage(3, 4), 75.0)
        self.assertEqual(calculate_percentage(0, 0), 0.0)

    def test_grade(self):
        self.assertEqual(get_grade(90), "Excellent!")
        self.assertEqual(get_grade(60), "Good effort, keep practising.")
        self.assertEqual(get_grade(10), "Needs more practice.")

    def test_categories_and_filter(self):
        self.assertEqual(get_categories(SAMPLE), ["Python", "Maths"])
        self.assertEqual(len(filter_questions(SAMPLE, "Python", None)), 1)
        self.assertEqual(len(filter_questions(SAMPLE, None, "Hard")), 1)
        self.assertEqual(len(filter_questions(SAMPLE, None, None)), 2)
        self.assertEqual(len(filter_questions(SAMPLE, "Python", "Hard")), 0)

    def test_fifty_fifty(self):
        for i in range(20):
            keep = fifty_fifty(SAMPLE[0])
            self.assertEqual(len(keep), 2)
            self.assertIn(SAMPLE[0]["answer"], keep)


class TestStorageParsing(unittest.TestCase):
    def test_question_round_trip(self):
        line = question_to_line(SAMPLE[0])
        self.assertEqual(parse_question_line(line), SAMPLE[0])

    def test_bad_question_line(self):
        self.assertIsNone(parse_question_line("only|three|parts"))
        self.assertIsNone(parse_question_line("q|a|b|c|d|x|cat|Easy"))

    def test_score_round_trip(self):
        score = {"date": "2026-01-01 10:00", "player": "Sam", "category": "All",
                 "score": 3, "total": 4, "percentage": 75.0, "seconds": 20}
        self.assertEqual(parse_score_line(score_to_line(score)), score)

    def test_bad_score_line(self):
        self.assertIsNone(parse_score_line("a|b|c"))


class TestAnalytics(unittest.TestCase):
    SCORES = [
        {"player": "A", "category": "Python", "percentage": 50.0, "seconds": 30},
        {"player": "A", "category": "Python", "percentage": 100.0, "seconds": 20},
        {"player": "B", "category": "Maths", "percentage": 100.0, "seconds": 10},
    ]

    def test_no_scores(self):
        self.assertIsNone(compute_stats([]))

    def test_stats(self):
        stats = compute_stats(get_player_scores(self.SCORES, "A"))
        self.assertEqual(stats["attempts"], 2)
        self.assertEqual(stats["average"], 75.0)
        self.assertEqual(stats["best"], 100.0)
        self.assertEqual(stats["average_time"], 25.0)
        self.assertEqual(stats["by_category"]["Python"], 75.0)

    def test_leaderboard_order(self):
        top = top_scores(self.SCORES, 2)
        self.assertEqual(top[0]["player"], "B")
        self.assertEqual(top[1]["seconds"], 20)


if __name__ == "__main__":
    unittest.main()
