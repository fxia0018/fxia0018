"""Refresh the upstream PR numbers in the profile card and the merged-PR table.

Run by .github/workflows/update-stats.yml. Uses only the standard library and
the GitHub REST API (GITHUB_TOKEN is optional but avoids rate limits).
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
ROOT = Path(__file__).resolve().parent.parent


def get(url: str):
    request = urllib.request.Request(url, headers={"Accept": "application/vnd.github+json"})
    token = os.environ.get("GITHUB_TOKEN")
    if token:
        request.add_header("Authorization", f"Bearer {token}")
    with urllib.request.urlopen(request, timeout=30) as response:
        return json.load(response)


def search(query: str) -> list[dict]:
    items: list[dict] = []
    page = 1
    while True:
        url = "https://api.github.com/search/issues?" + urllib.parse.urlencode(
            {"q": query, "sort": "created", "order": "desc", "per_page": 100, "page": page}
        )
        batch = get(url)["items"]
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


def short(n: int) -> str:
    if n >= 10_000:
        return f"{n / 1000:.0f}k"
    if n >= 1_000:
        return f"{n / 1000:.1f}k"
    return str(n)


PREFIX = re.compile(r"^[a-z]+(\([^)]*\))?!?:\s*", re.I)


def md(text: str) -> str:
    """Escape the characters a PR title could turn into table breaks or bold text."""
    return re.sub(r"([\\`*_|<>\[\]])", r"\\\1", text)


def merged_table(merged: list[dict]) -> str:
    """One row per project, most-starred first; each PR listed by its title."""
    by_repo: dict[str, list[dict]] = {}
    for item in merged:
        by_repo.setdefault(repo_of(item), []).append(item)
    stars = {repo: get(f"https://api.github.com/repos/{repo}")["stargazers_count"] for repo in by_repo}
    rows = ["| Project | What I fixed |", "|:--|:--|"]
    for repo in sorted(by_repo, key=lambda r: -stars[r]):
        prs = sorted(by_repo[repo], key=lambda i: -i["number"])
        fixes = "<br>".join(
            f"[#{i['number']}]({i['html_url']}) {md(PREFIX.sub('', i['title']))}" for i in prs
        )
        rows.append(f"| **[{repo}](https://github.com/{repo})**<br><sub>★ {short(stars[repo])}</sub> | {fixes} |")
    return "\n".join(rows)


def main() -> None:
    opened = upstream(search(f"is:pr author:{USER}"))
    merged = upstream(search(f"is:pr is:merged author:{USER}"))

    for name in ("card-dark.svg", "card-light.svg"):
        path = ROOT / "assets" / name
        text = path.read_text(encoding="utf-8")
        text = re.sub(r'(id="n-opened">)\d+<', rf"\g<1>{len(opened)}<", text)
        text = re.sub(r'(id="n-merged">)\d+<', rf"\g<1>{len(merged)}<", text)
        path.write_text(text, encoding="utf-8")

    readme = ROOT / "README.md"
    text = readme.read_text(encoding="utf-8")
    text = re.sub(
        r"\d+ PRs opened, \d+ merged upstream",
        f"{len(opened)} PRs opened, {len(merged)} merged upstream",
        text,
    )
    text = re.sub(
        r"(<!-- merged:start -->\n).*?(<!-- merged:end -->)",
        lambda m: m.group(1) + merged_table(merged) + "\n" + m.group(2),
        text,
        flags=re.S,
    )
    readme.write_text(text, encoding="utf-8")
    print(f"opened={len(opened)} merged={len(merged)}")


if __name__ == "__main__":
    main()
