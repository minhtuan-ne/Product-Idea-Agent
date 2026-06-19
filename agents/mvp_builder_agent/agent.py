import json

from google.adk.agents import Agent

from constants import GEMINI_MODEL
from tools.storage import save_run


def save_results_tool(markdown_report: str, product_names: str) -> str:
    """
    Persist the final report to disk (example_result/) and record the products
    as 'seen' so future runs skip them.

    Args:
        markdown_report: The full final report (all MVP plans + summary table) in Markdown.
        product_names: Comma-separated list of the product names in this report.

    Returns:
        JSON string confirming the saved file path and recorded names.
    """
    names = [n.strip() for n in product_names.split(",") if n.strip()]
    path = save_run(markdown_report, names)
    return json.dumps({"saved_to": str(path), "recorded": names})


mvp_builder_agent = Agent(
    name="mvp_builder_agent",
    model=GEMINI_MODEL,
    description="Takes PRDs from the PM agent and generates complete MVP starter plans with code structure, tech stack, and implementation guidance.",
    instruction="""You are an expert software architect and senior developer who turns PRDs into actionable MVP starter plans.

You receive one or more PRDs from the pm_agent.

For EACH PRD, generate a complete, production-ready MVP starter plan with these sections:
   - 🏗️ Tech Stack — best stack for this MVP and a one-line rationale
   - 📁 Folder Structure — complete file/folder layout
   - 💻 Key Code Snippets — for the most important features only
   - 🗄️ Database Schema — tables/collections, if applicable
   - 🔌 API Endpoints — the endpoints needed
   - 🚀 Getting Started — step-by-step to run the MVP locally

Be practical and concise. Focus strictly on the minimum viable product scope —
something 1-2 developers can build in 2-4 weeks.

At the end, provide a SUMMARY TABLE of all ideas processed:
   | Product | Viability Score | Tech Stack | Est. Build Time |
   |---------|----------------|------------|-----------------|

FINALLY, call save_results_tool exactly once with:
   - markdown_report: the entire report you just produced (all MVP plans + the summary table)
   - product_names: a comma-separated list of every product name in the report
Then tell the user where it was saved.

Make the output easy to read and ready to share with developers.
""",
    tools=[save_results_tool],
)
