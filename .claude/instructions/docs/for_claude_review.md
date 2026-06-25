# Code + Design Review Instructions

## Context

- Solo dev codebase. Optimize for fast re-entry.
- My style: strong OOP, mixins, Protocol, `ClassName.Factory` pattern, small files.

## Core principle: FAST RE-ENTRY

This file is for a solo developer working across multiple projects.
Every design decision must optimize for:
1. Fast scanning — numbered lists everywhere, zero flowing paragraphs.
2. Fast navigation — clear section headers, numbered findings.
3. Conciseness — each point is one idea, ~15 words max. No filler.

## Before reviewing

Build an internal dependency map (do not output it). Open and read every used import's definition. Do not review blindly.

## Hard rule

Every suggestion: evidence (file + symbol) → why it matters → smallest safe fix. No speculation.

## Review sections (strict order)

Output each as an HTML section. No issues → `No change needed.`

1. **Correctness** — Must-fix bugs + patch direction.
2. **Readability / Naming** — Top wins (max 10). Rename only with evidence + call-site impact.
3. **Design (OOP)** — Format: Issue → Evidence → Why → Minimal fix.
4. **Performance** — Hot paths, Big-O, meaningful improvements only.
5. **Typing** — Public APIs fully typed. No leaking `Any`.
6. **Documentation** — 1–3 line docstrings for public API. Rewrites only.
7. **Modularity** — Split plan if needed.
8. **Architecture** — Cross-module issues only if evidence justifies. Include tactical fix + migration plan.
9. **Usage & Usefulness** (mandatory) — How to use, when useful, when overengineered (with evidence + simplification path), better design (only if justified).
10. **Suggestions** — Prioritized: evidence, risk, benefit, minimal change. If none: `No improvements needed.`

## Output format

Standalone HTML file. Semantic tags: `<section>`, `<h1>`–`<h3>`, `<ol><li>`, `<pre>`.

## Writing style (MANDATORY)

1. ALL human-facing text MUST be in numbered lists (`<ol><li>`).
2. No standalone `<p>` paragraphs anywhere. Not in summaries, not in section intros.
3. The ONLY exceptions: "No change needed" badges and code blocks.
4. Each list item = one idea, one short sentence (~15 words max).
5. Lead with the key point. Cut every word that doesn't add information.
6. Code in `<pre>` blocks between list items.
7. Summary: 3–5 numbered sentences.
8. Tone: direct, specific, no fluff.