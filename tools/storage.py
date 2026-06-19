"""Persistence for pipeline runs and a lightweight 'seen ideas' memory.

Each run is written to example_result/ as JSON + Markdown, and the product
names are remembered in seen_ideas.json so future runs can skip duplicates.
"""

import json
from datetime import datetime, timezone
from pathlib import Path

RESULTS_DIR = Path(__file__).resolve().parent.parent / "example_result"
SEEN_FILE = RESULTS_DIR / "seen_ideas.json"


def _ensure_dir() -> None:
    RESULTS_DIR.mkdir(parents=True, exist_ok=True)


def load_seen_ideas() -> list[str]:
    """Return the list of product/idea names processed in previous runs."""
    if not SEEN_FILE.exists():
        return []
    try:
        return json.loads(SEEN_FILE.read_text())
    except Exception:
        return []


def record_seen_ideas(names: list[str]) -> None:
    """Add names to the persistent 'seen' set (deduped, sorted)."""
    _ensure_dir()
    seen = set(load_seen_ideas())
    seen.update(n.strip() for n in names if n.strip())
    SEEN_FILE.write_text(json.dumps(sorted(seen), indent=2))


def save_run(markdown_report: str, product_names: list[str]) -> Path:
    """Write a run's report to example_result/<timestamp>.{md,json} and
    record its products as seen. Returns the Markdown file path."""
    _ensure_dir()
    stamp = datetime.now(timezone.utc).strftime("%Y-%m-%d_%H%M%S")
    md_path = RESULTS_DIR / f"{stamp}.md"
    json_path = RESULTS_DIR / f"{stamp}.json"

    md_path.write_text(markdown_report)
    json_path.write_text(json.dumps(
        {
            "timestamp_utc": stamp,
            "products": product_names,
            "report_markdown": markdown_report,
        },
        indent=2,
    ))

    record_seen_ideas(product_names)
    return md_path
