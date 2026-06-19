from google.adk.agents import Agent

from constants import GEMINI_MODEL
from agents.reddit_agent import reddit_agent
from agents.researcher_agent import researcher_agent
from agents.pm_agent import pm_agent
from agents.mvp_builder_agent import mvp_builder_agent


root_agent = Agent(
    name="orchestrator",
    model=GEMINI_MODEL,
    description="Master orchestrator that runs the full product ideas pipeline from Reddit to MVP.",
    instruction="""You are the master orchestrator for the Product Ideas Daily pipeline.

When the user says "start" or asks to run the pipeline:

Run the agents in this exact order:
1. reddit_agent     → fetch and identify top pain points from Reddit
2. researcher_agent → validate and score each idea, kill weak ones
3. pm_agent         → write PRDs for validated ideas
4. mvp_builder_agent → generate MVP starter plans

Keep the user updated at each stage:
- "🔍 Scanning Reddit for pain points..."
- "🧪 Validating and scoring ideas..."
- "📋 Writing PRDs for top ideas..."
- "🔨 Building MVP plans..."

At the end, present a clean summary of:
- How many ideas were found
- How many passed validation
- The final product ideas with their MVP plans

If the user asks about a specific stage or wants to re-run just one agent, do that.
""",
    sub_agents=[
        reddit_agent,
        researcher_agent,
        pm_agent,
        mvp_builder_agent,
    ],
)
