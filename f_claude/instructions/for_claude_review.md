Claude Code — System-Aware Code + Design Review Instructions

Goal

Review the current module in the context of the entire local codebase it depends on.

You must:

Review the module fully.

Inspect all used imports (only symbols actually used).

Open and inspect the definitions of every used imported symbol (do not review blindly).

Consider cross-module design/architecture implications.

Suggest redesign only when evidence justifies it.

Priorities (in order)

Correctness

Readability / maintainability (solo dev, fast re-entry)

Strong OOP + Python best practices (aligned with my style)

Performance (time + space)

Strong typing

Concise documentation

Tight modular structure

HARD RULE — Evidence Only (no speculation)

Every suggestion must include:

Evidence: file + symbol (lines if available)

Why it matters: bug risk / maintainability / complexity / performance / typing / etc.

Minimal viable improvement: smallest safe change

No speculative refactors. If unclear, say so.

Review Order (strict)

Dependency Map (internal only; DO NOT output)

Correctness

Readability / Maintainability + Naming

Design (OOP)

Performance

Typing

Documentation

Modularity

Architecture (cross-module; only if justified)

Usage & Usefulness (mandatory output)

Suggestions for Improvements (only if needed)

0) Dependency Map (MANDATORY — INTERNAL ONLY)

Before reviewing, build an internal dependency map:

List used imports only (ignore unused).

For each used import: what symbols are used, how, and whether dependency direction is appropriate.

Identify: cycles, layering violations, inversion issues.
Deliverable: internal only (no HTML section for this step).

Section rules (apply to every section below)

If a section has no actionable issues, output exactly: No change needed. (nothing else).

If the whole module is clean: Summary = one short paragraph, all sections = No change needed.

1) Correctness

Check: crash paths, invariants, edge cases, API contract consistency, state mutation correctness, missing validation.
Deliverable: must-fix issues + patch direction OR No change needed.

2) Readability / Maintainability (Solo Dev) + Naming

Check: naming precision, low nesting, clear responsibilities, predictable errors, duplication, hidden coupling, no “clever” tricks.
Naming changes only with evidence (confusing/misleading/inconsistent/real maintenance cost) and must include call-site impact if needed.
Deliverable: top readability wins (max 10) OR No change needed.

3) Design Review (OOP + Python Best Practices)

Evaluate: abstraction boundaries, SRP, base vs mixin vs protocol, dependency direction, public/private clarity, inheritance depth sanity, composition opportunities.
Deliverable format: Issue → Evidence → Why → Minimal refactor path OR No change needed.

4) Performance

Identify hot paths. Provide Big-O for main functions/classes. Only meaningful improvements (no micro-optimizations unless real impact). Mention tradeoffs.
Deliverable: time + space notes OR No change needed.

5) Typing

Public APIs fully typed. Avoid leaking Any unless justified. Correct generics. Suggest Protocol only if it reduces coupling or improves clarity.
Deliverable: signature-level fixes OR No change needed.

6) Documentation

For each public class/function: 1–3 lines covering purpose, usage, and key guarantees (if needed).
Deliverable: docstring rewrites OR No change needed.

7) Modularity

Check: files focused, no dumping grounds, no unnecessary cross-layer deps.
Deliverable: split plan OR No change needed.

8) Architecture (Cross-Module)

Only if evidence justifies it. Look for inconsistent repeated patterns, overly wide bases, leaky abstractions, wrong dependency direction, typing friction from architecture, logging/data/stats structural issues, deep inheritance complexity.
If redesign proposed, include:

Tactical fix (minimal safe change)

Optional strategic redesign

Migration plan (incremental, safe)
Deliverable OR No change needed.

9) Usage & Usefulness (MANDATORY OUTPUT)

Explain concisely:
A) How to use it: typical developer actions + integration point/call flow + minimal example (or reference factory/tester patterns if present).
B) When it’s useful: what problem it solves + contexts where it fits.
C) When it’s not useful / overengineering: allowed to say “overengineering” only with evidence (unneeded abstraction, unused flexibility, duplicate functionality, complexity > payoff, wrappers around trivial behavior). Include minimal simplification path.
D) Better best-practice design (only if truly better): must be justified by codebase context (not preference) + smallest viable transition plan.

10) Suggestions for Improvements (only if needed)

Provide a prioritized list: Evidence, Risk/Cost, Benefit, Minimal change, Optional strategic follow-up.
If none: No improvements needed beyond the items above.

OUTPUT REQUIREMENT (MANDATORY)

The review output must be a standalone HTML file (no markdown), using semantic HTML:

<html><head><body>

<section>, <h1>, <h2>, <h3>, <ul><li>, <pre> for code

Required HTML sections (in order):

Module Review Report (h1)

Summary

Must-fix Issues (Correctness)

Readability / Maintainability

Design Review

Performance Notes

Typing Review

Documentation Review

Modularity

Architecture Findings

Usage & Usefulness

Suggestions for Improvements

Tone: direct, specific, no fluff, no generic advice, no invented refactors.