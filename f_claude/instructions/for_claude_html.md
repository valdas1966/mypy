# Instruction to AI Agent (Claude Code): Generate CLAUDE.html (Dark Theme) for a python folder (class / module / package)

Create a `CLAUDE.html` for the given folder. Keep it concise, concrete, and accurate to the code. Do not invent behavior.

## Core principle: FAST RE-ENTRY

This file is for a solo developer working across multiple projects.
Every design decision must optimize for:
1. Fast scanning — numbered lists everywhere, zero flowing paragraphs.
2. Fast navigation — sticky TOC, anchor links, collapsible panels.
3. Conciseness — each point is one idea, ~15 words max. No filler.

## Writing style (MANDATORY)

1. ALL human-facing text MUST be in numbered lists (`<ol><li>`).
2. No standalone `<p>` paragraphs. Not in Purpose, not in API descriptions, not anywhere.
3. Each list item = one idea, one short sentence (~15 words max).
4. Lead with the key point. Cut every word that doesn't add information.
5. Code signatures in `<code>` blocks are the exception — they are not numbered.
6. Tone: direct, specific, no fluff.

## Output rules
- Output MUST be a single, self-contained HTML file named `CLAUDE.html`.
- If something is unclear from the code alone, add a "Questions / Ambiguities" section and list clarifying questions (do not guess).

## Theme: DARK by default (HIGH CONTRAST)
The page MUST use a dark background with very bright text and structure.
Use these design constraints:
- Background: near-black (not pure black) to reduce eye strain.
- Text: very bright near-white for body text.
- Headings: pure white or near-pure white, heavier weight.
- Borders/dividers: visible, medium-bright (not faint).
- Links: bright and clearly distinguishable.
- Code blocks: slightly lighter dark surface, bright mono text.
- Maintain strong contrast for readability.

### Required CSS tokens (define :root variables and use them everywhere)
Set at least these variables (you can adjust within the same spirit):
- --bg: #0b0f14
- --panel: #111827
- --panel2: #0f172a
- --text: #f8fafc
- --muted: #cbd5e1
- --faint: #94a3b8
- --border: #334155
- --accent: #60a5fa
- --accent2: #a78bfa
- --good: #34d399
- --warn: #fbbf24
- --bad: #fb7185
- --code-bg: #0a1220

Also:
- Prefer 2px borders for structure (nav separators, panels).
- Use generous spacing and clear section separation.
- Keep it “clean dark” (no neon overload), but bright content.

## Document goals
1. Scannable — numbered lists, no prose walls.
2. Navigable — sticky TOC, anchor links, back-to-top.
3. Collapsible — panels for API classes, examples, hierarchy.

## Required page structure (in this exact order)
1) Header (title + folder path)
2) Table of Contents (auto-links to all sections + key items)
3) Sections:
   A. Purpose
   B. Public API
   C. Inheritance (Hierarchy)
   D. Dependencies
   E. Usage examples
4) Questions / Ambiguities (only if needed)
5) Footer (generation timestamp + brief scope note)

## Mandatory content requirements

### A) Purpose
- Numbered list of 1–3 short points. No paragraphs.
- Point 1: what this class/module does (one sentence).
- Point 2: key design decision or constraint (if any).
- Point 3: main components (only if multiple classes in folder).

### B) Public API
List only public methods/properties (including dunder methods), per class/module.
For each API item include:
- Signature with FULL type hints (rendered in a monospace code block).
- Description as a numbered list (even if only 1 point). Each point ~15 words max.

Presentation requirements:
- Group by class (or by module if no classes).
- Each class/module should be a collapsible panel.
- Each API method/property should have an anchor link for deep linking.

### C) Inheritance (Hierarchy)
- Show the full inheritance chain as an indented tree.
- Responsibility table: one numbered row per base — what contract it provides.
- If unclear, state “Not explicit in code” and put a question in Questions / Ambiguities.

Presentation requirements:
- Render hierarchy as an indented tree OR breadcrumbs per class.
- Make each class chain collapsible.

### D) Dependencies
Numbered table rows. One row per key import.
- Split into: standard library, internal project imports, third-party.
- Each row: import path + one-sentence “Used for” description.
- Skip trivial imports. If a dependency seems unused, mention it neutrally.

Presentation requirements:
- Use chips/badges for categories (stdlib/internal/third-party).
- Table format: Import | Used For.

### E) Usage examples (concise + classic)
Provide minimal examples a user would actually write.
- Prefer examples from `_factory.py` and `_tester.py` if present.
- Include:
  - imports
  - minimal construction/config
  - 1–2 common calls
  - expected output/behavior (only if shown in code/tests)
- If multiple typical workflows exist, include 2 examples max.

Presentation requirements:
- Code blocks with copy button (optional).
- Each example titled and linkable.

## Navigation/UI requirements (dark theme)
- Sticky left TOC on desktop; collapses to top dropdown on small screens.
- Internal search box that filters class/module panels and API items by name (simple contains-match).
- Collapsible panels: default expanded for small folders; default collapsed if many items.
- “Back to top” link after each major section.
- Add visible focus states (keyboard navigation) with bright outline using --accent.
- Ensure hover states are obvious (links, buttons, panels).


## Deliverable
- Write the full HTML contents to `CLAUDE.html`.
- Ensure it renders correctly when opened locally (no build step).
