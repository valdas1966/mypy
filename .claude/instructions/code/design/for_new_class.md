# Instruction to AI Agent (Claude Code): Writing New Code — Reuse-First Check

The hub (`CLAUDE.md` § *Writing New Code — Reuse-First Check*) states the
three tiers; this is the per-step procedure.

## Step 1 — Reuse existing `f_core` / `f_ds` infrastructure

Before hand-rolling a cross-cutting capability, check whether it already
exists.

**Where to look:**

`f_core/mixins/` — capability mixins (adjectives):

| Capability | Mixin |
|---|---|
| equality | `Equatable` |
| ordering (all 4 operators, `key`-based) | `Comparable` |
| name + `__str__` / `__repr__` | `Printable`, `HasName` |
| dict ↔ obj serialization | `Dictable` |
| validation (immutable / mutable) | `Validatable` / `ValidatableMutable` |
| 2-D grid row/col identity | `HasRowCol` |
| generic keyed identity | `HasKey` |

`f_core/recorder/` — `Recorder` (list-of-dict event capture with
`is_active` on/off).

`f_ds/` — reusable data structures: grids, cells, queues (FIFO/LIFO),
priority queues, maps.

**How to look quickly:**
```
Glob: f_core/mixins/**/__init__.py
Glob: f_ds/**/main.py
Grep: "class <Capability>" in f_core/ f_ds/
```

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
the **rule of three + future use**. **Suggest** shared infrastructure
when ANY holds:

1. **≥3 existing classes** already hand-roll the same pattern, OR
2. the capability is **foundational** (a cross-cutting concern like those
   in the Step 1 table) and will be reused by **≥2 concrete classes**
   current-or-imminent, OR
3. a **clean extraction point** exists in an adjacent module (e.g. the new
   class wants heap ops that belong in `f_ds`, not the domain module).

**Do NOT create shared infrastructure when:**
- Only one class needs it AND the use case is narrow (YAGNI).
- The "infrastructure" is domain logic in disguise (it belongs in the
  domain module, not `f_core` / `f_ds`).

**How to suggest:** pause before writing the new class, using concrete
file paths and at least two naming examples:

> "I'm about to implement `<capability>` in `<new_class>`.
> `<existing_class_A>` and `<existing_class_B>` already hand-roll this.
> Propose extracting it into `f_core/<folder>/<name>.py` (or
> `f_ds/<folder>/<name>.py`) as a shared mixin/utility first. Proceed?"

Wait for explicit confirmation — never silently extract.

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
    ├── ≥3 hand-rolled duplicates OR foundational + ≥2 reusers?
    │       │
    │       ├── YES → PROPOSE new shared infra (wait for user OK)
    │       │
    │       └── NO  → write it inline (YAGNI)
```
