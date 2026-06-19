"""Shared constants and tunable knobs for the pipeline."""

# Single model used across all agents — change here to swap models everywhere.
# Flash-Lite is the lightest free-tier model and has the most headroom against
# the free-tier rate limit. Bump to "gemini-3.5-flash" for higher quality if you
# enable billing or hit fewer 429s.
GEMINI_MODEL = "gemini-2.5-flash-lite"

# Hacker News tags to scan for product ideas / pain points.
#   ask_hn  -> people asking for help / describing problems
#   show_hn -> projects people built (competitive + novelty signal)
# (Dropped the noisy generic "story" feed to keep prompts small and save quota.)
DEFAULT_HN_TAGS = ["ask_hn", "show_hn"]

# Default number of posts to fetch per tag. Kept small to limit model calls /
# prompt size and stay under the free-tier rate limit.
DEFAULT_POST_LIMIT = 10

# How many days back to look.
DEFAULT_LOOKBACK_DAYS = 7

# Ideas scoring below this viability threshold are killed by the researcher agent.
VIABILITY_THRESHOLD = 5.5
