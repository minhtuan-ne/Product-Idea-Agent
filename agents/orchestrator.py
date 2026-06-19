from google.adk.agents import SequentialAgent

from agents.reddit_agent import reddit_agent
from agents.researcher_agent import researcher_agent
from agents.pm_agent import pm_agent
from agents.mvp_builder_agent import mvp_builder_agent


# Runs the pipeline deterministically in this exact order, every time:
# reddit -> researcher -> pm -> mvp_builder. Each agent's output feeds the next.
root_agent = SequentialAgent(
    name="orchestrator",
    description="Runs the full product ideas pipeline in order: Reddit -> Researcher -> PM -> MVP builder.",
    sub_agents=[
        reddit_agent,
        researcher_agent,
        pm_agent,
        mvp_builder_agent,
    ],
)
