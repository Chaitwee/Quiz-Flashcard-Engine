"""Module 4: Score history, statistics, leaderboard."""
import logging

from src import storage
from src.utils import get_yes_no


def get_player_scores(scores, player):
    return [s for s in scores if s["player"] == player]


def compute_stats(scores):
    """Return a dictionary of statistics, or None if there are no scores."""
    if len(scores) == 0:
        return None

    percentages = [s["percentage"] for s in scores]
    seconds = [s["seconds"] for s in scores]

    by_category = {}
    for s in scores:
        cat = s["category"]
        if cat not in by_category:
            by_category[cat] = []
        by_category[cat].append(s["percentage"])

    category_average = {}
    for cat in by_category:
        values = by_category[cat]
        category_average[cat] = round(sum(values) / len(values), 2)

    return {
        "attempts": len(scores),
        "average": round(sum(percentages) / len(percentages), 2),
        "best": max(percentages),
        "worst": min(percentages),
        "average_time": round(sum(seconds) / len(seconds), 1),
        "by_category": category_average,
    }


def score_sort_key(score):
    """Higher percentage first; if equal, faster time first."""
    return (-score["percentage"], score["seconds"])


def top_scores(scores, how_many):
    return sorted(scores, key=score_sort_key)[:how_many]


def show_analytics(player):
    scores = get_player_scores(storage.load_scores(), player)
    print("\n--- Score Analytics for " + player + " ---")
    stats = compute_stats(scores)
    if stats is None:
        print("No quiz attempts yet.")
        return

    print("Total attempts :", stats["attempts"])
    print("Average score  :", str(stats["average"]) + "%")
    print("Best score     :", str(stats["best"]) + "%")
    print("Worst score    :", str(stats["worst"]) + "%")
    print("Average time   :", stats["average_time"], "seconds")
    print("Average by category:")
    for cat in stats["by_category"]:
        print("  " + cat + ": " + str(stats["by_category"][cat]) + "%")

    print("\nLast 5 attempts:")
    for s in scores[-5:]:
        print("  " + s["date"] + " | " + s["category"] + " | " +
              str(s["score"]) + "/" + str(s["total"]) + " | " + str(s["seconds"]) + "s")


def show_leaderboard():
    scores = storage.load_scores()
    print("\n--- Leaderboard (Top 5) ---")
    if len(scores) == 0:
        print("No quiz attempts yet.")
        return
    for rank, s in enumerate(top_scores(scores, 5), start=1):
        print(str(rank) + ". " + s["player"] + " - " + str(s["percentage"]) + "% (" +
              str(s["seconds"]) + "s, " + s["category"] + ")")


def clear_history(player):
    scores = storage.load_scores()
    mine = get_player_scores(scores, player)
    if len(mine) == 0:
        print("You have no history to clear.")
        return
    if not get_yes_no("Delete all " + str(len(mine)) + " of your attempts? (y/n): "):
        print("Cancelled.")
        return
    others = [s for s in scores if s["player"] != player]
    if storage.save_scores(others):
        logging.info("Cleared history for %s", player)
        print("History cleared.")
