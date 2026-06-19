# Product Ideas Daily 🚀

An AI pipeline that scans Hacker News for pain points, validates ideas, writes PRDs, and generates MVP starter plans — powered entirely by Google Gemini via the Agent Development Kit (ADK).

## Pipeline

```
HN Agent → Researcher Agent → PM Agent → MVP Builder
```

1. **HN Agent** — Scans Hacker News (Ask HN, Show HN, top stories) for pain points and complaints
2. **Researcher Agent** — Validates ideas via Google Search and scores viability (kills weak ideas)
3. **PM Agent** — Writes scoped PRDs for top validated ideas
4. **MVP Builder Agent** — Generates complete MVP starter plans (tech stack, structure, code)

## Requirements

- Python 3.12+
- Google Gemini API key (used by every agent)

That's it — the Hacker News source uses the free, open [Algolia HN Search API](https://hn.algolia.com/api), so it needs **no API key, no account, and no approval**.

## Setup

```bash
# 1. Clone the repo
git clone <your-repo>
cd product-ideas-agent

# 2. Install dependencies
uv sync

# 3. Set up environment variables
cp .env.example .env
# Edit .env and add your GEMINI_API_KEY

# 4. Run
adk web
```

Then open the browser, type **"start"** and watch the pipeline run.

## Environment Variables

| Variable | Description |
|----------|-------------|
| `GEMINI_API_KEY` | Google Gemini API key (powers all agents) |

Get a key from [Google AI Studio](https://aistudio.google.com/apikey).

## Project Structure

```
product-ideas-agent/
├── agents/
│   ├── orchestrator.py          # Sequential pipeline runner
│   ├── hn_agent/                # Fetches Hacker News posts
│   │   ├── __init__.py          #   thin re-export
│   │   └── agent.py             #   agent + tool definition
│   ├── researcher_agent/        # Validates + scores ideas
│   ├── pm_agent/                # Writes PRDs
│   └── mvp_builder_agent/       # Generates MVP plans
├── tools/
│   └── hackernews_tool.py       # Free Algolia HN Search API wrapper
├── config.py                    # Typed settings (pydantic-settings)
├── constants.py                 # HN tags, model, thresholds
├── main.py                      # ADK entry point
├── pyproject.toml
└── .env.example
```

## Configuration

All tunable knobs live in [`constants.py`](constants.py):

```python
GEMINI_MODEL = "gemini-2.0-flash"          # swap the model everywhere
DEFAULT_HN_TAGS = ["ask_hn", "show_hn", "story"]  # which HN feeds to scan
DEFAULT_POST_LIMIT = 30                    # posts per tag
DEFAULT_LOOKBACK_DAYS = 7                  # how far back to look
VIABILITY_THRESHOLD = 5.5                  # lower to pass more ideas, raise to be stricter
```

The Gemini API key is read via [`config.py`](config.py) (typed `pydantic-settings`),
which loads from your `.env` file automatically.
