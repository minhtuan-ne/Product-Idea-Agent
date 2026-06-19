# Product Ideas Daily 🚀

An AI pipeline that scans Hacker News for pain points, validates ideas, writes PRDs, and generates MVP starter plans — powered entirely by Google Gemini via the Agent Development Kit (ADK).

## Pipeline

A `SequentialAgent` orchestrator runs five specialized agents in a fixed order. Each agent's output feeds the next.

```mermaid
flowchart LR
    Start([User: start]) --> HN

    subgraph orchestrator["Orchestrator (SequentialAgent)"]
        direction LR
        HN["HN Agent"]
        Researcher["Researcher Agent"]
        Scorer["Scorer Agent"]
        PM["PM Agent"]
        MVP["MVP Builder"]
        HN --> Researcher --> Scorer --> PM --> MVP
    end

    MVP --> Done([Saved report])
```

### What each agent does

| Step | Agent | Role | Output |
|------|-------|------|--------|
| 1 | **HN Agent** | Scans Hacker News for pain points and complaints | Top 5 raw product ideas |
| 2 | **Researcher Agent** | Validates ideas via Google Search (competitors, market signals) | Research notes per idea |
| 3 | **Scorer Agent** | Scores viability and filters weak ideas | Top 3 ideas (score ≥ 5.5) |
| 4 | **PM Agent** | Writes scoped PRDs for survivors | Structured PRDs |
| 5 | **MVP Builder** | Generates starter plans and saves results | MVP plans + summary table |

### Tools & external services

```mermaid
flowchart TB
    subgraph hn["HN Agent"]
        HN_Agent[HN Agent]
        Seen["get_seen_ideas_tool"]
        Fetch["fetch_posts_tool"]
        HN_Agent --> Seen
        HN_Agent --> Fetch
    end

    subgraph researcher["Researcher Agent"]
        Res_Agent[Researcher Agent]
        GSearch["google_search"]
        Res_Agent --> GSearch
    end

    subgraph scorer["Scorer Agent"]
        Score_Agent[Scorer Agent]
        ScoreFn["score_idea"]
        Score_Agent --> ScoreFn
    end

    subgraph pm["PM Agent"]
        PM_Agent[PM Agent]
        PRD["format_prd"]
        PM_Agent --> PRD
    end

    subgraph mvp["MVP Builder"]
        MVP_Agent[MVP Builder]
        Save["save_results_tool"]
        MVP_Agent --> Save
    end

    Fetch --> Algolia[(Algolia HN API)]
    Seen --> Disk1[(seen_ideas.json)]
    GSearch --> Google[(Google Search)]
    Save --> Disk2[(example_result/)]

    hn -->|"5 ideas"| researcher
    researcher -->|"research notes"| scorer
    scorer -->|"top 3"| pm
    pm -->|"PRDs"| mvp
```

> **Why two research steps?** Gemini does not allow built-in tools (`google_search`) and custom function tools (`score_idea`) in the same agent request. The researcher handles web search; the scorer handles deterministic scoring.

### Data flow (one run)

```mermaid
sequenceDiagram
    actor User
    participant Orch as Orchestrator
    participant HN as HN Agent
    participant Res as Researcher
    participant Scr as Scorer
    participant PM as PM Agent
    participant MVP as MVP Builder
    participant Store as example_result/

    User->>Orch: start
    Orch->>HN: run
    HN->>HN: skip seen ideas, fetch posts
    HN-->>Res: 5 pain-point ideas

    loop each idea
        Res->>Res: google_search competitors & market
    end
    Res-->>Scr: ideas + research notes

    loop each idea
        Scr->>Scr: score_idea (viability)
    end
    Scr-->>PM: top 3 (score ≥ 5.5)

    loop each idea
        PM->>PM: format_prd
    end
    PM-->>MVP: PRDs

    MVP->>MVP: generate MVP plans
    MVP->>Store: save_results_tool
    MVP-->>User: report path + summary table
```

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
│   ├── researcher_agent/        # Validates ideas via Google Search
│   ├── scorer_agent/            # Scores viability, filters to top 3
│   ├── pm_agent/                # Writes PRDs
│   └── mvp_builder_agent/       # Generates MVP plans
├── tools/
│   ├── hackernews_tool.py       # Free Algolia HN Search API wrapper
│   └── storage.py               # Saves runs + "seen ideas" memory
├── example_result/              # Saved run outputs (.json/.md) + seen_ideas.json
├── config.py                    # Typed settings (pydantic-settings)
├── constants.py                 # HN tags, model, thresholds
├── main.py                      # ADK entry point
├── pyproject.toml
└── .env.example
```

## Configuration

All tunable knobs live in [`constants.py`](constants.py):

```python
GEMINI_MODEL = "gemini-2.5-flash-lite"      # swap the model everywhere
DEFAULT_HN_TAGS = ["ask_hn", "show_hn"]     # which HN feeds to scan
DEFAULT_POST_LIMIT = 10                      # posts per tag
DEFAULT_LOOKBACK_DAYS = 7                    # how far back to look
VIABILITY_THRESHOLD = 5.5                    # lower to pass more ideas, raise to be stricter
```

The Gemini API key is read via [`config.py`](config.py) (typed `pydantic-settings`),
which loads from your `.env` file automatically.

> **Free-tier note:** the defaults are intentionally small to stay under Gemini's
> free-tier rate limit (~10 requests/min). If you hit `429 RESOURCE_EXHAUSTED`,
> wait a minute and rerun, lower these further, or enable billing. `flash-lite`
> is used for the most throughput; bump `GEMINI_MODEL` to `gemini-3.5-flash` for
> higher quality once you have headroom.

## Results & memory

Each run is saved to `example_result/` as both `.json` and `.md` (timestamped),
so you build a growing library of ideas. Product names are also recorded in
`example_result/seen_ideas.json`, and the HN agent checks this on every run to
**skip ideas it has already surfaced** — so repeat runs produce fresh ideas
instead of the same ones.
