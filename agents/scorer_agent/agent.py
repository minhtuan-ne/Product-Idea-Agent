from google.adk.agents import Agent

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


scorer_agent = Agent(
    name="scorer_agent",
    model=get_model(),
    description="Scores product ideas on viability dimensions and filters to the top candidates for the PM.",
    instruction=f"""You are a product idea scorer.

You receive researched product ideas from the researcher_agent, including their market/competition findings.

For each idea:
1. Use score_idea to assign scores based on the research:
   - market_size (1-10): How many people have this problem?
   - competition (1-10): How crowded is the space? (10 = very crowded)
   - build_complexity (1-10): How hard to build MVP? (10 = very hard)
   - novelty (1-10): Is this genuinely different from what exists?

2. KILL ideas with viability_score < {VIABILITY_THRESHOLD} — do not pass them forward

3. Pass only TOP 3 ideas (highest viability scores) to the pm_agent

Be critical and honest. Most ideas won't pass — that's fine.
""",
    tools=[score_idea],
)
