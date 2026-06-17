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
Pure prose compression — do **not** re-run work, re-read files, or call
tools.

## What to produce

1. **Lead with the answer.** First line = the verdict / direct answer. No
   preamble, no restating the question.
2. **Cut, don't drop.** Remove recaps, hedging, narration, repeated
   framing. Keep all substance — conclusions, caveats, numbers, paths,
   commands.
3. **Shortest faithful form.** A one-liner beats a paragraph if it fully
   answers.
4. **No new work.** Add no facts, options, or analysis absent from the
   original. A wrong original is a correction, not a `/tldr`.

## Length control (optional arg)

| Arg | Target |
|-----|--------|
| (none) | As short as stays faithful — typically ≤ 5 bullets |
| `one-line` / `1` | A single sentence |
| `N` (a number) | At most N bullets / N short lines |

## Guardrail

If the previous response was *already* concise, say so in one line rather
than padding it back out — do not invent length to justify the skill.
