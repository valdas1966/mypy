---
name: tldr
description: >-
  Rewrite the immediately-preceding assistant response in a shorter, simpler,
  more concise form — same substance, far fewer words. Trigger when the user
  says "/tldr", "tldr", "too long", "shorten that", "simpler", "give me the
  short version", or otherwise asks to compress the last reply. This is a
  momentary focusing lens, not a standing style: the default voice is natural;
  /tldr narrows it on demand. Optional arg sets the target length
  (e.g. "/tldr 3" = at most 3 bullets, "/tldr one-line" = a single sentence).
---

# tldr — compress my last response

Re-emit the **immediately-preceding assistant message** in a tighter form.
This is a pure prose-compression pass over what was already said — it does
**not** re-run work, re-read files, or call tools.

## Philosophy

The default voice is whatever is natural for the answer. Skills like this
one are **focusing lenses** the user applies *in the moment* to steer that
voice. `/tldr` is the "make it short" lens — reach for it when the previous
reply was longer or more elaborate than the user wanted right now.

## What to produce

1. **Lead with the answer.** First line = the verdict / result / direct
   answer. No preamble, no restating the question.
2. **Cut, don't drop.** Remove padding: recaps, hedging, narration,
   throat-clearing, repeated framing. Keep every piece of *substance* —
   conclusions, critical caveats, concrete numbers, file paths, commands.
   Compression is about phrasing, never about losing information the user
   needs.
3. **Prefer the shortest faithful form.** A single sentence or a few bullets
   beats paragraphs. If a one-liner fully answers it, give the one-liner.
4. **No new work.** Do not introduce facts, options, or analysis that were
   not in the original response. If the original was wrong, that is a
   separate correction — not a `/tldr`.

## Length control (optional arg)

| Arg | Target |
|-----|--------|
| (none) | As short as stays faithful — typically ≤ 5 bullets |
| `one-line` / `1` | A single sentence |
| `N` (a number) | At most N bullets / N short lines |

## Guardrail

If the previous response was *already* concise, say so in one line rather
than padding it back out — do not invent length to justify the skill.
