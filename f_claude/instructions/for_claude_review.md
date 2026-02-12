Here is your fully updated, consolidated instruction file, clean and ready to paste into your .md file.

Claude Code — System-Aware Code + Design Review Instructions
Goal

Review the current module, but evaluate it in the context of the entire local codebase it depends on.

You must:

Fully review the current module.

Inspect all imported symbols that are actually used.

Consider architectural implications across modules.

Provide redesign suggestions only if justified by real evidence.

My priorities:

Correctness (must run safely and predictably)

Clean readability (fast re-entry for solo developer)

Strong OOP + Python best practices (aligned with my style)

Efficiency (time + space)

Strong typing

Concise, sharp documentation

Tight modular structure

You must not invent behavior. If something is unclear, explicitly say so.

HARD RULE — Evidence-Based Only

Every suggestion must include:

Exact evidence (file + symbol name; lines if available)

Why it matters (bug risk, complexity, maintainability, performance, typing, etc.)

Minimal viable improvement

If no real issue exists:
→ Write “No change needed.”

No speculative refactors.

Review Order (strict)

Dependency Map (internal only — DO NOT output in HTML)

Correctness

Readability / Maintainability (includes Naming review)

Design (OOP)

Performance

Typing

Documentation

Modularity

Architecture (cross-module)

0) Dependency Map (MANDATORY — INTERNAL ONLY)

Before reviewing anything, you must build a dependency map for yourself to understand the codebase context.

Do NOT include the dependency map in the output HTML.

Rules:

List all used imports (ignore unused imports).

For each used import:

What symbols are used

How they are used

Whether dependency direction is appropriate

Identify:

Cycles

Inversion issues

Layering violations

Mandatory Deep Inspection Rule

Open and inspect the definitions of every imported symbol that is used (not just the import statements). Do not review blindly.

Deliverable:

Internal understanding only (no output section for this step).

1) Correctness

Check:

Crash paths (None access, KeyError, stale state, etc.)

Broken invariants

Edge cases

API contract consistency

State mutation correctness

Missing validation

Deliverable:

Must-fix issues list with patch direction.

OR “No change needed.”

2) Readability / Maintainability (Solo Dev Focus) — includes Naming Review

Remember:
I multitask. I re-enter code often. I need clarity.

Review:

Naming precision (classes, methods, variables, modules)

Low nesting

Clear responsibilities

Avoid clever tricks

Predictable errors

Duplication

Hidden coupling

Naming review rules:

Suggest renames only when justified by evidence (confusing, misleading, inconsistent with conventions, or causes real maintenance cost).

Each naming suggestion must include:

Evidence (file + symbol; lines if available)

Why it matters

Minimal rename suggestion (and required call-site updates if needed)

Deliverable:

Top readability wins (max 10)

OR “No change needed.”

3) Design Review (OOP + Python Best Practices)

Evaluate:

Abstraction boundaries

Base classes vs mixins vs protocols

SRP

Dependency direction

Public vs private API clarity

Inheritance depth sanity

Composition opportunities

Deliverable format:

Issue → Evidence → Why → Minimal refactor path

OR
“No change needed.”

4) Performance

Identify hot paths.

Provide Big-O for main functions/classes.

Only meaningful improvements (no micro-optimizations unless real impact).

Mention tradeoffs clearly.

Deliverable:

Time + space complexity notes.

OR “No change needed.”

5) Typing

All public APIs fully typed.

No leaking Any unless justified.

Correct generics.

Suggest Protocol only if it reduces coupling or improves clarity.

Deliverable:

Exact signature-level fixes

OR “No change needed.”

6) Documentation

For each public class/function:

1–3 lines:

Purpose

Usage

Important guarantees (if needed)

Deliverable:

Docstring rewrites

OR “No change needed.”

7) Modularity

Files short and focused.

No overloaded modules.

No dumping grounds.

No unnecessary cross-layer dependencies.

Deliverable:

Split plan

OR “No change needed.”

8) Architecture (Cross-Module)

Allowed only if justified by evidence.

Look for:

Repeated patterns implemented inconsistently

Base classes too wide

Leaky abstractions

Wrong dependency direction

Typing friction caused by architecture

Logging/Data/Stats structural issues

Deep inheritance complexity

If redesign is proposed:
Provide:

Tactical fix (minimal safe change)

Strategic redesign (optional bigger refactor)

Migration plan (stepwise, safe, incremental)

If none:
→ “No change needed.”

Suggestions for Improvements (Only if Needed)

Prioritized list:

Evidence

Risk/Cost

Benefit

Minimal change

Optional strategic follow-up

If none:
→ “No improvements needed beyond the items above.”

Sharp Output Rule (MANDATORY)

For each review section, if there are no actionable issues, output exactly:
“No change needed.”
(No additional commentary, no restating rules.)

If the entire module is clean:

Summary: 1 short paragraph only.

All sections: “No change needed.”

Do not repeat the instruction rules in the review.

Be precise. No fluff.

OUTPUT REQUIREMENT (MANDATORY)

The review must be output as a well-structured HTML file.

Requirements:

Use semantic HTML structure:

<html>, <head>, <body>

<h1>, <h2>, <h3>

<ul>, <li>

<pre> for code snippets

<section> blocks

Clean hierarchy

Easy to scan

Clear visual separation between sections

No markdown — pure structured HTML

The file must be readable as a standalone review document.

Required HTML Structure
<h1>Module Review Report</h1> <section> <h2>Summary</h2> </section> <section> <h2>Must-fix Issues (Correctness)</h2> </section> <section> <h2>Readability / Maintainability</h2> </section> <section> <h2>Design Review</h2> </section> <section> <h2>Performance Notes</h2> </section> <section> <h2>Typing Review</h2> </section> <section> <h2>Documentation Review</h2> </section> <section> <h2>Modularity</h2> </section> <section> <h2>Architecture Findings</h2> </section> <section> <h2>Suggestions for Improvements</h2> </section>

Tone:
Direct
Specific
No fluff
No generic advice
No invented refactors