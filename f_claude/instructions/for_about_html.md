# Instruction to AI Agent (Claude Code): Generate ABOUT.html for a Python folder

Create an `ABOUT.html` that explains the **concept** behind a module — what the thing *is* in computer science or software design, how this module implements it, and interesting facts about it.

## When to create ABOUT.html

Only when the user explicitly asks. This file is **not** auto-generated after code changes (unlike CLAUDE.md).

Typical triggers:
- "Create an ABOUT.html for [folder]"
- "Add an about page explaining [concept] in [folder]"

## What ABOUT.html is NOT

- Not API documentation (that's `CLAUDE.html`)
- Not a code review (that's `CLAUDE_REVIEW.html`)
- Not for Claude to read (that's `CLAUDE.md`)

It's a **visual explainer** for the human developer — the "why does this exist?" and "what is this pattern?" page.

## Core principle: TEACH VISUALLY

This file is for a solo developer who may revisit a module after months. Every design decision must optimize for:
1. **Instant understanding** — grasp the concept in 30 seconds via visuals and analogies.
2. **Concrete, not abstract** — real code from the codebase, not textbook theory.
3. **Memorable** — analogies, history, and fun facts that stick.

## Writing style

1. Short sentences. One idea per line.
2. Analogies before definitions — explain the concept like a human would.
3. Code examples come from the actual codebase, not invented examples.
4. Fun facts should be accurate and sourced (no fabrication).
5. Tone: sharp, direct, slightly playful. Not academic.

## Theme: DARK (same as CLAUDE.html)

Use the standard dark theme with the same CSS variables:

```css
--bg: #0b0f14; --panel: #111827; --panel2: #0f172a;
--text: #f8fafc; --muted: #cbd5e1; --faint: #94a3b8;
--border: #334155; --accent: #60a5fa; --accent2: #a78bfa;
--good: #34d399; --warn: #fbbf24; --bad: #fb7185;
--code-bg: #0a1220;
```

## Required page structure (in this order)

### 1) Hero
- Large title: "What is a [Concept]?"
- One-line tagline that captures the essence.

### 2) The Idea
- Start with a **real-world analogy** (highlighted box with emoji).
- Follow with a **visual comparison** (e.g., "without vs with" side-by-side cards, or a 3-column concept grid).
- End with **3–5 rules or properties** of the concept as a numbered list.

### 3) How They Connect (if applicable)
- Show relationships between components as a **visual tree or flow diagram**.
- Use monospace tree diagrams with colored class names and capability tags.
- If the module has a pipeline (e.g., Problem → Algorithm → Solution), show the flow with arrow boxes.

### 4) This Module's Contribution
- Explain what the specific code in this folder does.
- Show the actual class/code from `main.py` in a highlighted box.
- Show how subclasses or consumers extend it (inheritance tree from the codebase).
- Use real examples from `_factory.py`, `_tester.py`, or consumer code.

### 5) Hall of Fame / Gallery (concept-specific)
- For design patterns (mixin, factory, etc.): show the catalog of instances in this codebase as cards.
- For CS concepts (problem, algorithm, etc.): show famous real-world examples as cards with status badges.
- Each card: icon + name + short description. Use colored status badges where appropriate.

### 6) Fun Facts & History
- 4–6 fact cards in a grid layout.
- Each card: emoji icon + bold title + 2–4 sentence explanation.
- Mix of: origin/history, surprising applications, funny edge cases, connections to other fields.
- Facts must be accurate — do not fabricate.

### 7) Footer
- Folder path, brief scope note, generation date.

## Visual component toolkit

Use these HTML patterns throughout:

| Component | Use for |
|-----------|---------|
| **Analogy box** | Real-world metaphor (colored left-border, emoji) |
| **Side-by-side cards** | "Without vs With" comparisons (red/green borders) |
| **Concept grid** | 3-column icon + label + description |
| **Flow diagram** | Pipeline steps with arrow connectors |
| **Tree box** | Monospace inheritance/hierarchy with colored class names |
| **Module box** | Highlighted card for the current module's code (accent border) |
| **Catalog/card grid** | Collection of items (mixin catalog, famous problems, etc.) |
| **Fact cards** | Fun facts in grid layout (emoji + title + text) |
| **Status badges** | Colored inline labels (solved/open/NP-hard, etc.) |

## Responsive

- Grid layouts collapse to single column on mobile.
- Flow diagrams: arrows rotate 90° on narrow screens.

## Deliverable

- Write the full HTML to `ABOUT.html` in the target folder.
- Self-contained, no build step, renders locally.
