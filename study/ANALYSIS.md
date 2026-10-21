# Wilson (u/ClaudeAI-mod-bot): voice analysis

Corpus: 68,888 comments, 2025-08-19 to 2026-10-21, from the Arctic Shift archive.
- 4,052 thread TL;DRs (Dec 2025 onward). This is the creative core.
- 92 free-form persona replies and `!AskWilson` answers.
- About 64,800 moderation messages (templated). Unique bodies: 15,618. Mostly rule decisions.

Identity: the bot's own reply settles it: "the name is Wilson". Users summon it with `!AskWilson` in megathreads.
Its real system prompt is **not public**. In the thread "How the F does the Claude TL;DR auto-bot work?"
nobody from the mod team disclosed it. Wilson's own TL;DR of that thread said its persona comes from "a system
prompt loaded with *examples* of my tone", not from a complex instruction. That is self-report, not evidence.

## Numbers (all 4,052 TL;DRs)

| Trait | Value |
|---|---|
| Header | `**TL;DR of the discussion generated automatically after N comments.**` (N = 30/40/50/100/200) |
| Body length | median ~180 words (p10 ≈ 760, p90 ≈ 1,690 chars). Flat across 11 months |
| Verdict inside first 2 sentences | 92% |
| Verdict carries **bold** | 88% |
| Opens with a short hook line, not the verdict | 37% (23% are ≤8 words) |
| Bulleted | 64%, median 3 bullets (max 16), each bullet starting with a **bold lead-in** |
| Paragraph blocks | median 4 |
| Quotes commenters verbatim | 87% of TL;DRs, median 2 quotes |
| Italic emphasis on single words | 48% |
| Second person ("you", "OP") | 84% ("OP" alone: 57%) |
| Bot talks about itself ("I'm") | 2%, mostly in meta threads |
| Em dash | 0.62 per 1k words (very low for an LLM) |
| "!" | 0.39 per 1k words |
| delve / tapestry / testament / landscape | ≈0 |

Stable across the whole period, which suggests one prompt with few revisions.

## The machine: why it reads well

1. **It summarises people, not content.** The thread is a character ("the thread ain't buying it", "the comment
   section quickly evolved into a healthy debate"). Factions get names ("The Agent Architects", "the skeptics",
   "the 'just talk to each other' camp"). It reports who believes what, and how strongly (top comment
   "by a landslide", "a few dissenters in the downvoted depths", "got nuked with downvotes").
2. **Verdict first, in bold.** The bold sentence is the TL;DR of the TL;DR. Someone who reads only the bold still
   gets the answer.
3. **A hook that sets the register in under 8 words.** "Whoa there, cowboy." "Alright, settle down, class."
   "Yeah, it's not just you." "Nah, the thread ain't buying it, OP." "Well, this is awkward." The stance is a
   teacher, bartender or sports commentator: affectionately exasperated and never sneering.
4. **It borrows the wit.** Most of the jokes are *quoted from commenters* ("Opus can prepare for litigation",
   "Next is the malware", "lipstick on a pig"). Wilson curates the funniest true line rather than inventing jokes.
   This is the single biggest anti-slop trick, because the humour is specific to the thread and could not be
   made up.
5. **Jokes at the edges, facts in the middle.** Bullets are dense and plain: numbers, commands in backticks,
   file names, the actual mechanism. Wit lives in the hook, the bullet labels ("The future is now, old man:",
   "Safeguards? What safeguards?:"), parentheticals ("looking at you, Avermedia capture card guy") and the closer.
6. **The turn.** After the verdict comes the complication: "However, the praise comes with a huge asterisk",
   "But the real buzzkill…", "That said…". Every summary has tension.
7. **A minority report.** Dissent always gets a line, sized honestly ("a few", "a strong minority").
8. **The closer** is one of three moves:
   - a short zinger ("Respect." "Simple as." "We see you."),
   - the verdict restated in plain words ("So, the community verdict is: …"),
   - a throwaway aside ("Oh, and a few people are convinced OP works for OpenAI.").
9. **Plain colloquial register**, with no corporate words: "cooked", "ain't", "nothingburger", "touch grass",
   "the deets". Contractions everywhere, a few rhetorical questions, almost no exclamation marks.
10. **Fair to the facts.** It corrects misinformation using the thread itself ("the thread schooled a few users on
    how VC funding works"), credits experts ("a user with a PhD in quantum computing hardware… broke it down for
    the class") and never invents a consensus the comments don't show.

## Selection rules (60 thread → TL;DR pairs, median 49 comments seen)

- **Quotes are mostly real.** Of 168 quoted phrases, 69% appear verbatim in the archived thread and 14% are
  reworded versions of real lines (every word appears in the thread). About 8% match neither. Those are scare
  quotes ('savage', 'manager') or possible inventions, and the archive may also miss deleted comments.
- **It quotes the top of the thread.** The median quoted comment sits at the top 18% by score, and 53% of quotes
  come from the top 20% of comments.
- **It doesn't restate the post.** Only 24% of the post's distinctive words reappear. The TL;DR is about the
  reaction.
- On average 45% of the words in the top 3 comments resurface in the TL;DR, so the top comments drive the
  summary.

## `!AskWilson` answer format (fixed spec, leaked by its consistency)

```
Hi u/<user>.

Wilson here, <one-line quip that names the user's pain in a fresh image>.

**The Problem**: <one-sentence restatement of the issue>

**What To Do:**
- **<Imperative label>:** <concrete step with the why>
- …

**How Confident am I?**: **High|Medium|Low**, <why, with the limit of what it knows>
```
Quip examples: "your friendly neighborhood context-cop"; "diving into the billing abyss so you don't have to";
"the digital equivalent of being trapped in an elevator…".

## Weaknesses (do NOT copy)

- **Formula fatigue.** "The consensus is that" appears in 921 TL;DRs, "a resounding yes" in 271, "as one user put
  it" in 207, and "Alright, let's break it down" repeats constantly. Any single summary feels fresh. Read 50 in a row
  and the frame shows. The skill must rotate frames.
- **Generic labels** ("The Good / The Bad", "The Fix") outnumber the inspired ones.
- **Model habits, not craft.** The `*   ` bullet (asterisk plus 3 spaces) appears in 100% of bulleted TL;DRs.
  That is a Gemini markdown signature, so Wilson probably runs on a Gemini model (an inference, not a fact).
  "Game-changer" (0.17 per 1k words) and the occasional "It's not X, it's Y" are the same kind of habit.
- **Stock cowboy hooks** ("Whoa there, cowboy/killer/champ/Nelly") start to blur together once you have read a few.

## Moderation voice

The rule decisions are dry legal-ish templates ("**The modbot's decision:** Fails criteria (e): uses promotional
language ("…")"), and they always quote the offending phrase as evidence. The charm lives in a few human-written
lines: "**ClaudeAI-mod-bot usage limit reached. Your post will be reviewed in 5 hours.** j/k! Relax. Just need to get
the humans to take a look at this…".
