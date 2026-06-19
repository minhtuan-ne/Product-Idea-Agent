"""Shared constants and tunable knobs for the pipeline."""

# Single model used across all agents — change here to swap models everywhere.
GEMINI_MODEL = "gemini-2.0-flash"

# Subreddits scanned for product ideas (names are case-insensitive, keep them unique).
DEFAULT_SUBREDDITS = [
    "SideProject",
    "startups",
    "entrepreneur",
    "productivity",
    "smallbusiness",
    "webdev",
    "learnprogramming",
]

# Default number of posts to fetch per subreddit.
DEFAULT_POST_LIMIT = 30

# Ideas scoring below this viability threshold are killed by the researcher agent.
VIABILITY_THRESHOLD = 5.5
