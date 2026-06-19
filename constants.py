"""Shared constants and tunable knobs for the pipeline."""

# Single model used across all agents — change here to swap models everywhere.
# gemini-3.5-flash is the current free-tier model (gemini-2.0-flash retired Mar 2026).
GEMINI_MODEL = "gemini-3.5-flash"

# Hacker News tags to scan for product ideas / pain points.
#   ask_hn  -> people asking for help / describing problems
#   show_hn -> projects people built (competitive + novelty signal)
#   story   -> general front-page stories
DEFAULT_HN_TAGS = ["ask_hn", "show_hn", "story"]

# Default number of posts to fetch per tag.
DEFAULT_POST_LIMIT = 30

# How many days back to look.
DEFAULT_LOOKBACK_DAYS = 7

# Ideas scoring below this viability threshold are killed by the researcher agent.
VIABILITY_THRESHOLD = 5.5
