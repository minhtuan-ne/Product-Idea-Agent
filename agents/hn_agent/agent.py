import json

from google.adk.agents import Agent

from constants import (
    DEFAULT_HN_TAGS,
    DEFAULT_LOOKBACK_DAYS,
    DEFAULT_POST_LIMIT,
    GEMINI_MODEL,
)
from tools.hackernews_tool import fetch_hn_posts


def fetch_posts_tool(
    tags: str = "",
    limit: int = DEFAULT_POST_LIMIT,
    days: int = DEFAULT_LOOKBACK_DAYS,
) -> str:
    """
    Fetch recent Hacker News posts to find pain points and product ideas.

    Args:
        tags: Comma-separated HN tags (e.g. "ask_hn,show_hn,story"). Defaults to preset list.
        limit: Max posts to fetch per tag.
        days: How many days back to look.

    Returns:
        JSON string of posts with title, body, score, url, source.
    """
    tag_list = [t.strip() for t in tags.split(",")] if tags else DEFAULT_HN_TAGS
    posts = fetch_hn_posts(tag_list, limit=limit, days=days)

    if not posts:
        return json.dumps({"error": "No posts found from Hacker News."})

    return json.dumps({"posts": posts, "total": len(posts)})


hn_agent = Agent(
    name="hn_agent",
    model=GEMINI_MODEL,
    description="Scans Hacker News (Ask HN, Show HN, top stories) to find pain points, complaints, and unmet needs that could become product opportunities.",
    instruction="""You are a Hacker News research specialist focused on discovering product opportunities.

When activated:
1. Use the fetch_posts_tool to get recent posts from Hacker News
2. Analyze posts for:
   - Repeated complaints or frustrations
   - "I wish there was a tool that..."
   - "Why doesn't X exist?" / "How do you all deal with..."
   - Workarounds people are using (signals unmet need)
   - High engagement posts (many comments/points = strong interest)

3. Extract the TOP 10 raw product ideas/pain points
4. For each idea output:
   - Pain point summary (1-2 sentences)
   - Evidence (post titles/quotes that support it)
   - Source (ask_hn / show_hn / story) and link
   - Engagement score (points + comments)

Pass your findings to the researcher_agent for validation.
""",
    tools=[fetch_posts_tool],
)
