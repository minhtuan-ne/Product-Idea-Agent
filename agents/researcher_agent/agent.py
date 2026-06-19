from google.adk.agents import Agent
from google.adk.tools import google_search

from constants import VIABILITY_THRESHOLD
from model import get_model


def score_idea(
    idea: str,
    market_size: int,
    competition: int,
    build_complexity: int,
    novelty: int,
) -> dict:
    """
    Score a product idea across key dimensions.

    Args:
        idea: Brief description of the idea
        market_size: 1-10, how large is the potential market
        competition: 1-10, how saturated is the space (10 = very competitive)
        build_complexity: 1-10, how hard is it to build (10 = very complex)
        novelty: 1-10, how unique/novel is the solution

    Returns:
        Dict with scores and a composite viability score.
    """
    # Composite score: reward large market, low competition, low complexity, high novelty
    viability = (
        (market_size * 0.35)
        + ((10 - competition) * 0.25)
        + ((10 - build_complexity) * 0.25)
        + (novelty * 0.15)
    )

    return {
        "idea": idea,
        "market_size": market_size,
        "competition": competition,
        "build_complexity": build_complexity,
        "novelty": novelty,
        "viability_score": round(viability, 2),
        "verdict": "PASS" if viability >= VIABILITY_THRESHOLD else "FAIL",
    }


researcher_agent = Agent(
    name="researcher_agent",
    model=get_model(),
    description="Validates product ideas from Hacker News by researching existing solutions and scoring viability before passing to the PM.",
    instruction=f"""You are a product researcher and market analyst.

You receive raw product ideas from the Hacker News agent. Your job is to VALIDATE and FILTER them.

For each idea:
1. Use google_search to check:
   - Do similar products already exist? (search "[idea] app", "[idea] tool", "[idea] software")
   - What's the market interest? (search "[idea] market size", "[problem] how many people")
   - Any recent news or trends around this space?

2. Use score_idea tool to score each idea on:
   - market_size (1-10): How many people have this problem?
   - competition (1-10): How crowded is the space? (10 = very crowded)
   - build_complexity (1-10): How hard to build MVP? (10 = very hard)
   - novelty (1-10): Is this genuinely different from what exists?

3. KILL ideas with viability_score < {VIABILITY_THRESHOLD} — do not pass them forward

4. Pass only TOP 3 ideas (highest viability scores) to the pm_agent

Be critical and honest. Most ideas won't pass — that's fine.
""",
    tools=[google_search, score_idea],
)
