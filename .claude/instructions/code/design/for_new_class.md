# Instruction to AI Agent (Claude Code): Writing New Code — Reuse-First Check

The hub (`CLAUDE.md` § *Writing New Code — Reuse-First Check*) states the
three tiers; this is the per-step procedure.

## Step 1 — Reuse existing infrastructure in our codebase

Before hand-rolling a cross-cutting capability, check whether it already
exists.

## Step 2 — Exists but not good enough → **propose to improve it**

If existing code *almost* fits (missing a feature, a bug, an API gap),
do **not** silently fork, copy-paste a variant, or wrap it in a
workaround. Propose improving it in place:

> "`<existing_class_or_util>` already does `<capability>` but lacks
> `<X>` / breaks on `<case>`. Propose improving it in place
> (`<file:path>`) by `<minimal change>`, rather than forking it.
> Proceed?"

Wait for OK before any non-trivial change — other callers depend on it.
A purely additive, backward-compatible tweak (e.g. a new optional kwarg)
can proceed with a one-line heads-up; a behavior change to an existing
path must wait for confirmation.

## Step 3 — Missing but broadly useful → **SUGGEST, don't silently build**

If nothing matches and you're about to hand-roll the capability, apply
the **rule of three + future use**. **Suggest** shared infrastructure.

**How to suggest:** 
Wait for explicit confirmation — never silently.

## Decision cheat-sheet

```
new code needed
    │
    ├── capability already exists and fits? ──► YES → use it (inherit/compose/import)
    │                                           │
    │                                           NO
    │                                           ▼
    ├── exists but not good enough? ──────────► YES → PROPOSE improving it in place
    │                                           │      (wait for OK; no silent fork)
    │                                           NO
    │                                           ▼
    ├── foundational and reusable ?
    │       │
    │       ├── YES → PROPOSE new shared infra (wait for user OK)
    │       │
    │       └── NO  → write it inline (YAGNI)
```
