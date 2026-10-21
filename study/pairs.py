"""Build thread -> TL;DR pairs: for a stratified sample of Wilson TL;DRs, fetch the post and
the comments that existed when the TL;DR was written. Output: corpus/pairs.jsonl (resumable).
"""
import json
import random
import time
import urllib.error
import urllib.request
from pathlib import Path

API = "https://arctic-shift.photon-reddit.com/api"
HERE = Path(__file__).parent
SRC = HERE / "corpus" / "tldr.jsonl"
OUT = HERE / "corpus" / "pairs.jsonl"
SAMPLE = 60
SEED = 21
PAUSE_S = 2.0
MAX_PAGES = 4


def get(path):
    req = urllib.request.Request(API + path, headers={"User-Agent": "style-research/0.1"})
    for attempt in range(8):
        try:
            with urllib.request.urlopen(req, timeout=120) as r:
                return json.loads(r.read().decode())["data"] or []
        except urllib.error.HTTPError as e:
            detail = e.read()[:80]
            print(f"HTTP {e.code} {detail!r} retry {attempt + 1}", flush=True)
            if e.code != 422 and e.code < 500:
                return []  # bad request: retrying won't help
        except (urllib.error.URLError, TimeoutError) as e:
            print(f"net {e} retry {attempt + 1}", flush=True)
        time.sleep(PAUSE_S * 4 * (attempt + 1))
    return []


def thread_comments(link, cutoff):
    """Page backward from the TL;DR timestamp: only what the bot could have seen."""
    out, before = [], cutoff
    for _ in range(MAX_PAGES):
        page = get(f"/comments/search?link_id={link}&limit=100&before={before}")
        time.sleep(PAUSE_S)
        if not page:
            break
        out += page
        before = min(c["created_utc"] for c in page)
    keep = ("id", "parent_id", "author", "body", "score", "created_utc")
    return [{k: c.get(k) for k in keep} for c in out if c["author"] != "ClaudeAI-mod-bot"]


def main():
    tldrs = [json.loads(line) for line in SRC.open(encoding="utf8")]
    random.Random(SEED).shuffle(tldrs)
    done = {json.loads(line)["tldr"]["id"] for line in OUT.open(encoding="utf8")} if OUT.exists() else set()
    with OUT.open("a", encoding="utf8") as f:
        for t in tldrs:
            if len(done) >= SAMPLE:
                break
            if t["id"] in done:
                continue
            link = t["link_id"][3:]
            post = get(f"/posts/ids?ids={link}")
            time.sleep(PAUSE_S)
            comments = thread_comments(link, t["created_utc"])
            if not post or len(comments) < 15:
                continue
            p = post[0]
            f.write(json.dumps({
                "tldr": t,
                "post": {k: p.get(k) for k in ("id", "title", "selftext", "author", "score", "link_flair_text")},
                "comments": comments,
            }, ensure_ascii=False) + "\n")
            f.flush()
            done.add(t["id"])
            print(f"{len(done)} pairs ({len(comments)} comments)", flush=True)


if __name__ == "__main__":
    main()
