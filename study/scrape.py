"""Pull every archived comment by u/ClaudeAI-mod-bot from the Arctic Shift Reddit archive.

Reddit itself blocks unauthenticated JSON, so the public archive is the source.
Output: corpus/raw.jsonl (one comment per line, verbatim body plus metadata). Resumable.
"""
import json
import sys
import time
import urllib.error
import urllib.request
from pathlib import Path

AUTHOR = "ClaudeAI-mod-bot"
API = "https://arctic-shift.photon-reddit.com/api/comments/search"
PAGE = 100
PAUSE_S = 1.5
MAX_RETRIES = 8
OUT = Path(__file__).parent / "corpus" / "raw.jsonl"
KEEP = ("id", "created_utc", "body", "link_id", "parent_id", "subreddit", "score", "permalink")


def fetch(before):
    url = f"{API}?author={AUTHOR}&limit={PAGE}" + (f"&before={before}" if before else "")
    req = urllib.request.Request(url, headers={"User-Agent": "style-research/0.1"})
    for attempt in range(MAX_RETRIES):
        try:
            with urllib.request.urlopen(req, timeout=90) as r:
                return json.loads(r.read().decode())["data"]
        except urllib.error.HTTPError as e:
            detail = e.read()[:120].decode("utf8", "replace")
            print(f"HTTP {e.code} {detail} (retry {attempt + 1})", flush=True)
        except (urllib.error.URLError, TimeoutError) as e:
            print(f"net error {e} (retry {attempt + 1})", flush=True)
        time.sleep(PAUSE_S * 4 * (attempt + 1))
    sys.exit(f"gave up at before={before}")


def main():
    OUT.parent.mkdir(exist_ok=True)
    seen, before = set(), None
    if OUT.exists():
        rows = [json.loads(line) for line in OUT.open(encoding="utf8")]
        seen = {r["id"] for r in rows}
        before = min((r["created_utc"] for r in rows), default=None)
    with OUT.open("a", encoding="utf8") as f:
        while True:
            page = [c for c in fetch(before) if c["id"] not in seen]
            if not page:
                break
            for c in page:
                seen.add(c["id"])
                f.write(json.dumps({k: c.get(k) for k in KEEP}, ensure_ascii=False) + "\n")
            before = min(c["created_utc"] for c in page)
            print(f"{len(seen)} comments, oldest {before}", flush=True)
            time.sleep(PAUSE_S)
    print(f"done: {len(seen)}")


if __name__ == "__main__":
    main()
