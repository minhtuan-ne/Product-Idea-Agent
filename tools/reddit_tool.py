import praw
from datetime import datetime, timedelta, timezone

from config import settings


def get_reddit_client() -> praw.Reddit:
    return praw.Reddit(
        client_id=settings.reddit_client_id,
        client_secret=settings.reddit_client_secret,
        user_agent=settings.reddit_user_agent,
    )


def fetch_reddit_posts(subreddits: list[str], limit: int = 50) -> list[dict]:
    """
    Fetch the last day's top posts from given subreddits.
    Returns a list of post dicts with title, body, score, url, subreddit.
    """
    reddit = get_reddit_client()
    yesterday = datetime.now(timezone.utc) - timedelta(days=1)
    posts = []

    for subreddit_name in subreddits:
        try:
            subreddit = reddit.subreddit(subreddit_name)
            for post in subreddit.top(time_filter="day", limit=limit):
                created = datetime.fromtimestamp(post.created_utc, tz=timezone.utc)
                if created >= yesterday:
                    posts.append({
                        "title": post.title,
                        "body": post.selftext[:500] if post.selftext else "",
                        "score": post.score,
                        "url": post.url,
                        "subreddit": subreddit_name,
                        "num_comments": post.num_comments,
                    })
        except Exception as e:
            print(f"Error fetching r/{subreddit_name}: {e}")

    # Sort by score descending
    posts.sort(key=lambda x: x["score"], reverse=True)
    return posts[:limit]
