"""Lint a draft for AI-slop markers and check its shape against Wilson-corpus norms.

Usage: python slop_check.py draft.md [--mode summary|answer|post]
Exit code 0 = clean, 1 = has FAIL findings. WARN findings are judgement calls.
Norms come from 4,052 real Wilson TL;DRs (see ANALYSIS.md in the study folder).
"""
import argparse
import re
import sys
from pathlib import Path

BANNED = {
    r"\bdelv(e|es|ing)\b": "delve",
    r"\btapestry\b": "tapestry",
    r"\btestament to\b": "testament to",
    r"\b(ever-evolving|ever-changing) landscape\b": "evolving landscape",
    r"\bnavigat(e|ing) the\b": "navigate the",
    r"\bseamless(ly)?\b": "seamless",
    r"\bgame[- ]?changer\b": "game-changer",
    r"\bleverag(e|ing)\b": "leverage",
    r"\belevat(e|es|ing)\b": "elevate",
    r"\bunlock(s|ing)? (the|your|new)\b": "unlock the",
    r"\brealm of\b": "realm of",
    r"\bin today's\b": "in today's…",
    r"\bit'?s worth noting\b": "it's worth noting",
    r"\bin conclusion\b": "in conclusion",
    r"\blet'?s dive in\b": "let's dive in",
    r"\bbuckle up\b": "buckle up",
    r"\bhere'?s the thing\b": "here's the thing",
    r"\bgreat question\b": "great question",
    r"\bthis thread discusses\b": "this thread discusses",
    r"\bnot just [^.,;]{1,40},? but\b": "not just X but Y",
    r"\bit'?s not [^.;]{1,40}[,;—–-]+ it'?s\b": "it's not X, it's Y",
    r"\bmay potentially\b": "may potentially",
}
# Wilson's own tics: fine once in a while, a tell when they repeat. Rotate the frame.
WILSON_TICS = {
    r"\bthe (overwhelming |general )?consensus (is|in|here)\b": "the consensus is",
    r"\bresounding\b": "resounding",
    r"\blet'?s (break|cut|get) (it|this|to)\b": "let's break it down",
    r"\bwhoa(,)? there\b": "whoa there",
    r"\bas one user put it\b": "as one user put it",
    r"\bthe general vibe\b": "the general vibe",
}
SHAPES = {
    "summary": {"words": (60, 330), "max_bullets": 7},
    "answer": {"words": (60, 260), "max_bullets": 5},
    "post": {"words": (60, 400), "max_bullets": 6},
}
WORDS_PER_EM_DASH = 150
EXCLAIM_MAX = 1
TRIAD_MAX = 1


def find_all(patterns: dict[str, str], text: str) -> list[str]:
    return [label for pat, label in patterns.items() if re.search(pat, text, re.I)]


def check(text: str, mode: str) -> list[tuple[str, str]]:
    out: list[tuple[str, str]] = []
    words = len(re.findall(r"\w+", text))
    lo, hi = SHAPES[mode]["words"]
    if not lo <= words <= hi:
        out.append(("WARN", f"{words} words; corpus range for {mode} is {lo}-{hi}"))
    for label in find_all(BANNED, text):
        out.append(("FAIL", f"slop phrase: {label}"))
    for label in find_all(WILSON_TICS, text):
        out.append(("WARN", f"Wilson tic, rotate the frame: {label}"))
    own_words = re.sub(r"[\"“][^\"”\n]*[\"”]", "", text)  # quoted lines are the source's punctuation
    dashes = own_words.count("—") + own_words.count(" – ")
    if dashes > max(1, words // WORDS_PER_EM_DASH):
        out.append(("FAIL", f"{dashes} em dashes in {words} words (Wilson: 0.6 per 1k)"))
    if own_words.count("!") > EXCLAIM_MAX:
        out.append(("WARN", f"{own_words.count('!')} exclamation marks; let the content carry the energy"))
    triads = re.findall(r"\b\w+(?: \w+)?, \w+(?: \w+)?,? and \w+", text)
    if len(triads) > TRIAD_MAX:
        out.append(("WARN", f"{len(triads)} rule-of-three lists; break the rhythm"))
    bullets = re.findall(r"^\s*[-*]\s+(.*)$", text, re.M)
    if len(bullets) > SHAPES[mode]["max_bullets"]:
        out.append(("WARN", f"{len(bullets)} bullets; cut to the ones that change a decision"))
    unlabelled = [b for b in bullets if not b.startswith("**")]
    if bullets and len(unlabelled) > len(bullets) // 2:
        out.append(("WARN", "most bullets lack a bold lead-in label"))
    if mode in ("summary", "answer"):
        head = " ".join(re.split(r"(?<=[.!?])\s+", text.strip())[:3])
        if "**" not in head:
            out.append(("FAIL", "no bold verdict in the first three sentences"))
    if mode == "summary" and not re.search(r"[\"“][^\"”\n]{3,90}[\"”]", text):
        out.append(("WARN", "no verbatim quote from the source; borrowed wit is the best wit"))
    if mode == "summary":
        own = re.sub(r"[\"“][^\"”\n]*[\"”]", "", text)
        addr = re.findall(r"\b(you|your|y'all|folks|we|us)\b|, OP\b|\bOP[,.!?]", own, re.I)
        if len(addr) < 2:
            out.append(("WARN", f"{len(addr)} direct addresses (you, OP, we); talk to the room, don't report on it"))
    return out


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("file")
    ap.add_argument("--mode", choices=SHAPES, default="summary")
    args = ap.parse_args()
    findings = check(Path(args.file).read_text(encoding="utf8"), args.mode)
    for level, msg in findings:
        print(f"{level}: {msg}")
    if not findings:
        print("clean")
    sys.exit(1 if any(level == "FAIL" for level, _ in findings) else 0)


if __name__ == "__main__":
    main()
