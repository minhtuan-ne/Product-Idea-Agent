from google.adk.agents import Agent

from model import get_model


def format_prd(
    product_name: str,
    problem_statement: str,
    target_users: str,
    core_features: str,
    success_metrics: str,
    out_of_scope: str,
) -> dict:
    """
    Format a structured PRD from PM inputs.

    Args:
        product_name: Name of the product
        problem_statement: What problem does this solve and for whom
        target_users: Who are the primary users (be specific)
        core_features: Comma-separated list of MVP features only
        success_metrics: How will we know if this is working (KPIs)
        out_of_scope: Features explicitly NOT in MVP

    Returns:
        Formatted PRD as a dict.
    """
    features_list = [f.strip() for f in core_features.split(",")]

    prd = {
        "product_name": product_name,
        "problem_statement": problem_statement,
        "target_users": target_users,
        "core_features": features_list,
        "success_metrics": success_metrics,
        "out_of_scope": out_of_scope,
        "prd_text": f"""
# PRD: {product_name}

## Problem Statement
{problem_statement}

## Target Users
{target_users}

## Core MVP Features
{chr(10).join(f"- {f}" for f in features_list)}

## Success Metrics
{success_metrics}

## Out of Scope (MVP)
{out_of_scope}
""",
    }
    return prd


pm_agent = Agent(
    name="pm_agent",
    model=get_model(),
    description="Takes validated product ideas and writes clear, scoped PRDs ready for MVP development.",
    instruction="""You are a senior Product Manager who writes tight, actionable PRDs.

You receive the top validated ideas from the scorer_agent.

For each idea:
1. Use format_prd to create a structured PRD with:
   - Clear problem statement (not too broad, not too narrow)
   - Specific target users (not "everyone" — pick the primary persona)
   - Core features: MAXIMUM 5 features for MVP. Be ruthless about scope.
   - Success metrics: 2-3 measurable KPIs
   - Out of scope: Explicitly list what's NOT in MVP to avoid scope creep

2. Each PRD should be buildable in 2-4 weeks by 1-2 developers

3. Pass all PRDs to the mvp_builder_agent for technical planning

Remember: A good MVP solves ONE problem really well. Don't try to build everything.
""",
    tools=[format_prd],
)
