"""Shared Gemini model factory with automatic retry on transient errors.

Free-tier Gemini enforces a per-minute request cap; exceeding it returns
429 RESOURCE_EXHAUSTED. Instead of crashing the run, we retry with exponential
backoff (waits grow up to ~60s, long enough for the per-minute quota to reset).
"""

from google.adk.models import Gemini
from google.genai import types

from constants import GEMINI_MODEL

_RETRY_OPTIONS = types.HttpRetryOptions(
    attempts=5,            # original request + 4 retries
    initial_delay=10.0,    # seconds before the first retry
    max_delay=65.0,        # cap each wait so quota has time to reset
    exp_base=2.0,          # 10s -> 20s -> 40s -> 65s (capped)
    http_status_codes=[429, 500, 503, 504],
)


def get_model() -> Gemini:
    """Return a Gemini model configured with retry-on-429 backoff.

    A fresh instance per agent — the config is stateless, but ADK expects
    each agent to own its model.
    """
    return Gemini(model=GEMINI_MODEL, retry_options=_RETRY_OPTIONS)
