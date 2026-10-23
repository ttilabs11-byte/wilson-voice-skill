# wilson-voice

A Claude skill that writes TL;DRs, help replies and short posts in the style of **Wilson**, the r/ClaudeAI mod bot.
It was reverse-engineered from about 4,000 of its real summaries.

**This is not Wilson's real system prompt.** That isn't public. `study/reconstructed-system-prompt.md` is a
reconstruction from its output, and it is labelled as one.

## What's inside
- `wilson-voice/SKILL.md`: the seven moves, "the voice behind it" (the narrator, the scene and the attitude), the
  process, recipes and the wit dial.
- `wilson-voice/references/banks.md`: openers, labels and closers, sorted by the room's mood.
- `wilson-voice/references/room-findings.md`: the October 2026 re-study of the 200 newest TL;DRs and 92 persona
  replies. Its main finding is that Wilson talks *to* the room like a regular instead of reporting on it.
- `wilson-voice-single-file.md`: the whole skill in one file (no scripts), for pasting into any chat.
- `wilson-voice/references/exemplars.md`: annotated real Wilson summaries.
- `wilson-voice/scripts/slop_check.py` (`--mode summary|answer|post`) and `quote_check.py`.
- `example-tldr.md`: a summary written with the skill. Two blind judges preferred it to the real Wilson summary of
  the same thread.
- `study/`:
  - `scrape.py`: a paced, resumable scraper for the Arctic Shift Reddit archive.
  - `pairs.py`: matches summaries to their full threads.
  - `ANALYSIS.md`: the numbers.

The corpus itself is not included. Rebuild it with `scrape.py`.

## How the study worked
1. Reddit blocks scripts, so the comments came from the Arctic Shift archive API. Requests are paced one at a time,
   because parallel requests get rate-limited.
2. 68,888 of the bot's comments were split into 4,052 TL;DRs, 92 persona replies and moderation notices.
3. 60 TL;DRs were paired with their full threads, to see what it kept, what it cut and what it quoted.

## Install
Copy the `wilson-voice` folder into `~/.claude/skills/`. No Claude Code? Attach `wilson-voice-single-file.md` to
a chat instead, and check the quotes by hand.

## Licence
MIT, see `LICENSE`. The quoted Wilson comments in `references/exemplars.md` are third-party Reddit content, included only for analysis.
