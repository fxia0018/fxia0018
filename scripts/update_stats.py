"""Refresh the upstream PR numbers and the recently-merged list in the profile.

Run by .github/workflows/update-stats.yml. Uses only the standard library and
the GitHub search API (GITHUB_TOKEN is optional but avoids rate limits).
"""

from __future__ import annotations

import json
import os
import re
import urllib.parse
import urllib.request
from pathlib import Path

USER = "fxia0018"
# Repositories that do not count as "upstream": my own, and a classmate's
# course project.
EXCLUDE_OWNERS = {USER}
EXCLUDE_REPOS = {"CaoLongyang/UM-Auto-Attendance"}
RECENT_COUNT = 6
ROOT = Path(__file__).resolve().parent.parent


def search(query: str) -> list[dict]:
    items: list[dict] = []
    page = 1
    while True:
        url = "https://api.github.com/search/issues?" + urllib.parse.urlencode(
            {"q": query, "sort": "created", "order": "desc", "per_page": 100, "page": page}
        )
        request = urllib.request.Request(url, headers={"Accept": "application/vnd.github+json"})
        token = os.environ.get("GITHUB_TOKEN")
        if token:
            request.add_header("Authorization", f"Bearer {token}")
        with urllib.request.urlopen(request, timeout=30) as response:
            batch = json.load(response)["items"]
        items.extend(batch)
        if len(batch) < 100 or page == 10:
            return items
        page += 1


def repo_of(item: dict) -> str:
    return item["repository_url"].split("/repos/", 1)[1]


def upstream(items: list[dict]) -> list[dict]:
    return [
        item
        for item in items
        if repo_of(item).split("/")[0] not in EXCLUDE_OWNERS and repo_of(item) not in EXCLUDE_REPOS
    ]


def main() -> None:
    opened = upstream(search(f"is:pr author:{USER}"))
    merged = upstream(search(f"is:pr is:merged author:{USER}"))
    merged.sort(key=lambda item: item["pull_request"]["merged_at"], reverse=True)

    for name in ("card-dark.svg", "card-light.svg"):
        path = ROOT / "assets" / name
        text = path.read_text(encoding="utf-8")
        text = re.sub(
            r"\d+ opened \| \d+ merged upstream",
            f"{len(opened)} opened | {len(merged)} merged upstream",
            text,
        )
        path.write_text(text, encoding="utf-8")

    readme = ROOT / "README.md"
    text = readme.read_text(encoding="utf-8")
    text = re.sub(
        r"\d+ PRs opened, \d+ merged upstream",
        f"{len(opened)} PRs opened, {len(merged)} merged upstream",
        text,
    )
    lines = []
    for item in merged[:RECENT_COUNT]:
        title = item["title"].replace("|", "\\|").replace("[", "\\[").replace("]", "\\]")
        day = item["pull_request"]["merged_at"][:10]
        lines.append(f"- `{day}` **{repo_of(item)}** · [{title}]({item['html_url']})")
    block = "\n".join(lines)
    text = re.sub(
        r"<!-- RECENT_MERGED:START -->.*?<!-- RECENT_MERGED:END -->",
        lambda m: f"<!-- RECENT_MERGED:START -->\n{block}\n<!-- RECENT_MERGED:END -->",
        text,
        flags=re.DOTALL,
    )
    readme.write_text(text, encoding="utf-8")
    print(f"opened={len(opened)} merged={len(merged)}")


if __name__ == "__main__":
    main()
