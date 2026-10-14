"""Langfuse issue radar.

Finds open Langfuse issues with no assignee and no linked PR, and comments the new
ones on a tracking issue in this repo, so GitHub notifies the owner by email.
Issues already reported are remembered in radar/seen.json (committed by the workflow).

Stdlib only. Needs GITHUB_TOKEN and GITHUB_REPOSITORY (both set by GitHub Actions).
"""

import datetime as dt
import json
import os
import pathlib
import urllib.parse
import urllib.request

UPSTREAM_REPOS = ["langfuse/langfuse"]  # all Langfuse issues, Python SDK included, live here
LOOKBACK_DAYS = int(os.environ.get("LOOKBACK_DAYS") or 3)
TRACKING_TITLE = "Langfuse issue radar"
SEEN_FILE = pathlib.Path(__file__).with_name("seen.json")

TOKEN = os.environ["GITHUB_TOKEN"]
REPO = os.environ["GITHUB_REPOSITORY"]
API = "https://api.github.com"


def call(method, path, body=None):
    req = urllib.request.Request(
        API + path,
        method=method,
        data=json.dumps(body).encode() if body is not None else None,
        headers={
            "Authorization": f"Bearer {TOKEN}",
            "Accept": "application/vnd.github+json",
            "X-GitHub-Api-Version": "2022-11-28",
        },
    )
    with urllib.request.urlopen(req, timeout=30) as resp:
        return json.load(resp)


def find_unclaimed():
    since = (dt.datetime.now(dt.timezone.utc) - dt.timedelta(days=LOOKBACK_DAYS)).date()
    found = []
    for repo in UPSTREAM_REPOS:
        q = f"repo:{repo} is:issue is:open no:assignee -linked:pr created:>={since}"
        res = call("GET", "/search/issues?" + urllib.parse.urlencode({"q": q, "per_page": 50}))
        found += res["items"]
    return found


def tracking_issue():
    issues = call("GET", f"/repos/{REPO}/issues?state=open&per_page=100")
    for issue in issues:
        if issue["title"] == TRACKING_TITLE and "pull_request" not in issue:
            return issue["number"]
    created = call(
        "POST",
        f"/repos/{REPO}/issues",
        {
            "title": TRACKING_TITLE,
            "body": "New Langfuse issues with no assignee and no linked PR are posted here "
            "as comments by `.github/workflows/langfuse-radar.yml`. Claim good ones fast: "
            "comment on the upstream issue with your planned fix.",
        },
    )
    return created["number"]


def line(item):
    labels = ", ".join(label["name"] for label in item["labels"]) or "no labels"
    return f"- [#{item['number']}]({item['html_url']}) {item['title']} ({labels}; opened {item['created_at'][:10]})"


def main():
    seen = set(json.loads(SEEN_FILE.read_text())) if SEEN_FILE.exists() else set()
    new = [item for item in find_unclaimed() if item["html_url"] not in seen]
    summary = os.environ.get("GITHUB_STEP_SUMMARY")
    if not new:
        print("No new unclaimed issues.")
        if summary:
            pathlib.Path(summary).write_text("No new unclaimed Langfuse issues.\n")
        return
    bugs = [i for i in new if any(label["name"] == "bug" for label in i["labels"])]
    rest = [i for i in new if i not in bugs]
    body = f"**{len(new)} new unclaimed Langfuse issue(s)**\n\n" + "\n".join(line(i) for i in bugs + rest)
    call("POST", f"/repos/{REPO}/issues/{tracking_issue()}/comments", {"body": body})
    print(body)
    if summary:
        pathlib.Path(summary).write_text(body + "\n")
    seen |= {item["html_url"] for item in new}
    SEEN_FILE.write_text(json.dumps(sorted(seen), indent=2) + "\n")


if __name__ == "__main__":
    main()
