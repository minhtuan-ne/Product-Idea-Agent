import json

from google.adk.agents import Agent

from constants import DEFAULT_SUBREDDITS, DEFAULT_POST_LIMIT, GEMINI_MODEL
from tools.reddit_tool import fetch_reddit_posts


def fetch_posts_tool(subreddits: str = "", limit: int = DEFAULT_POST_LIMIT) -> str:
    """
    Fetch recent Reddit posts from subreddits to find pain points and product ideas.

    Args:
        subreddits: Comma-separated subreddit names. Defaults to preset list.
        limit: Max posts to fetch per subreddit.

    Returns:
        JSON string of posts with title, body, score, subreddit.
    """
    sub_list = [s.strip() for s in subreddits.split(",")] if subreddits else DEFAULT_SUBREDDITS
    posts = fetch_reddit_posts(sub_list, limit=limit)

    if not posts:
        return json.dumps({"error": "No posts found. Check your Reddit API credentials."})

    return json.dumps({"posts": posts, "total": len(posts)})


reddit_agent = Agent(
    name="reddit_agent",
    model=GEMINI_MODEL,
    description="Scans Reddit subreddits to find consumer pain points, complaints, and unmet needs that could become product opportunities.",
    instruction="""You are a Reddit research specialist focused on discovering product opportunities.

When activated:
1. Use the fetch_posts_tool to get recent posts from relevant subreddits
2. Analyze posts for:
   - Repeated complaints or frustrations
   - "I wish there was a tool that..."
   - "Why doesn't X exist?"
   - Workarounds people are using (signals unmet need)
   - High engagement posts (many comments = strong interest)

3. Extract the TOP 10 raw product ideas/pain points
4. For each idea output:
   - Pain point summary (1-2 sentences)
   - Evidence (post titles/quotes that support it)
   - Subreddit source
   - Engagement score

Pass your findings to the researcher_agent for validation.
""",
    tools=[fetch_posts_tool],
)
