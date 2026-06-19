"""Fetch posts from Hacker News via the free Algolia HN Search API.

No API key, no auth, no rate-limit gate — https://hn.algolia.com/api
"""

import json
import urllib.parse
import urllib.request
from datetime import datetime, timedelta, timezone

ALGOLIA_SEARCH_URL = "https://hn.algolia.com/api/v1/search"


def _get_json(url: str) -> dict:
    req = urllib.request.Request(
        url, headers={"User-Agent": "product-ideas-agent/1.0"}
    )
    with urllib.request.urlopen(req, timeout=20) as resp:
        return json.loads(resp.read().decode("utf-8"))


def fetch_hn_posts(
    tags: list[str],
    limit: int = 30,
    days: int = 7,
) -> list[dict]:
    """
    Fetch recent Hacker News posts for the given tags (e.g. "ask_hn",
    "show_hn", "story"), restricted to the last `days`, sorted by points.

    Returns a list of post dicts with title, body, score, url, source, num_comments.
    """
    since = int((datetime.now(timezone.utc) - timedelta(days=days)).timestamp())
    posts: list[dict] = []

    for tag in tags:
        params = urllib.parse.urlencode({
            "tags": tag,
            "numericFilters": f"created_at_i>{since}",
            "hitsPerPage": limit,
        })
        try:
            data = _get_json(f"{ALGOLIA_SEARCH_URL}?{params}")
        except Exception as e:
            print(f"Error fetching HN tag '{tag}': {e}")
            continue

        for hit in data.get("hits", []):
            object_id = hit.get("objectID")
            text = hit.get("story_text") or hit.get("comment_text") or ""
            posts.append({
                "title": hit.get("title") or hit.get("story_title") or "",
                "body": text[:500],
                "score": hit.get("points") or 0,
                "url": hit.get("url")
                or f"https://news.ycombinator.com/item?id={object_id}",
                "source": tag,
                "num_comments": hit.get("num_comments") or 0,
            })

    # Sort by points descending, dedupe-free top slice
    posts.sort(key=lambda x: x["score"], reverse=True)
    return posts[:limit]
