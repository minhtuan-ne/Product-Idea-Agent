# Product Ideas Daily 🚀

An AI pipeline that scans Reddit for pain points, validates ideas, writes PRDs, and generates MVP starter plans — powered entirely by Google Gemini via the Agent Development Kit (ADK).

## Pipeline

```
Reddit Agent → Researcher Agent → PM Agent → MVP Builder
```

1. **Reddit Agent** — Scans subreddits for consumer pain points and complaints
2. **Researcher Agent** — Validates ideas via Google Search and scores viability (kills weak ideas)
3. **PM Agent** — Writes scoped PRDs for top validated ideas
4. **MVP Builder Agent** — Generates complete MVP starter plans (tech stack, structure, code)

## Requirements

- Python 3.12+
- Google Gemini API key (used by every agent)
- Reddit API credentials

## Setup

```bash
# 1. Clone the repo
git clone <your-repo>
cd product-ideas-agent

# 2. Install dependencies
uv sync

# 3. Set up environment variables
cp .env.example .env
# Edit .env with your API keys

# 4. Run
adk web
```

Then open the browser, type **"start"** and watch the pipeline run.

## Environment Variables

| Variable | Description |
|----------|-------------|
| `GEMINI_API_KEY` | Google Gemini API key (powers all agents) |
| `REDDIT_CLIENT_ID` | Reddit app client ID |
| `REDDIT_CLIENT_SECRET` | Reddit app client secret |
| `REDDIT_USER_AGENT` | Reddit user agent string |

### Getting Reddit API credentials

1. Go to https://www.reddit.com/prefs/apps
2. Click "create another app"
3. Select "script"
4. Fill in name and redirect URI (use `http://localhost:8080`)
5. Copy the client ID (under app name) and secret

## Project Structure

```
product-ideas-agent/
├── agents/
│   ├── orchestrator.py          # Master orchestrator
│   ├── reddit_agent/            # Fetches Reddit posts
│   │   ├── __init__.py          #   thin re-export
│   │   └── agent.py             #   agent + tool definition
│   ├── researcher_agent/        # Validates + scores ideas
│   ├── pm_agent/                # Writes PRDs
│   └── mvp_builder_agent/       # Generates MVP plans
├── tools/
│   └── reddit_tool.py           # PRAW Reddit wrapper
├── config.py                    # Typed settings (pydantic-settings)
├── constants.py                 # Subreddits, model, thresholds
├── main.py                      # ADK entry point
├── pyproject.toml
└── .env.example
```

## Configuration

All tunable knobs live in [`constants.py`](constants.py):

```python
GEMINI_MODEL = "gemini-2.0-flash"   # swap the model everywhere
DEFAULT_SUBREDDITS = [...]          # which subreddits to scan
DEFAULT_POST_LIMIT = 30             # posts per subreddit
VIABILITY_THRESHOLD = 5.5           # lower to pass more ideas, raise to be stricter
```

Credentials and API keys are read via [`config.py`](config.py) (typed `pydantic-settings`),
which loads from your `.env` file automatically.
