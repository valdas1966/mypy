# Code + Design Review Instructions

## Context

- Solo dev codebase. Optimize for fast re-entry.
- My style: strong OOP, mixins, Protocol, `ClassName.Factory` pattern, small files.

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

Writing style:
- Every finding = short numbered sentence (one idea, ~15 words max).
- `<ol>` is the primary structure. No long paragraphs.
- Lead with the key point. No filler.
- Code in `<pre>` blocks between list items.
- Summary: 3–5 numbered sentences.
- Tone: direct, specific, no fluff.