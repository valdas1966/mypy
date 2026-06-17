# Instruction to AI Agent (Claude Code): Building a New Class — Infrastructure Check

Before writing a new class, run this **2-step check**. It is a
pre-coding gate, same category as *Clarify Before Acting*. The
codebase's primary design language is capability-as-mixin +
reusable-data-structure — silently re-implementing a capability
fragments the framework (future migrations become N-class
refactors).

## Step 1 — Reuse existing `f_core` / `f_ds` infrastructure

Before hand-rolling **any** cross-cutting capability (identity,
equality, ordering, serialization, validation, event capture,
container type), check whether it already exists.

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

`f_core/recorder/` — `Recorder` (list-of-dict event capture
with `is_active` on/off).

`f_ds/` — reusable data structures: grids, cells, queues
(FIFO/LIFO), priority queues, maps.

**How to look quickly:**
```
Glob: f_core/mixins/**/__init__.py
Glob: f_ds/**/main.py
Grep: "class <Capability>" in f_core/ f_ds/
```

**Rule:** if the capability exists, USE IT by inheritance or
composition. Never reimplement `__eq__` / `__hash__` / ordering
/ recording / heap ops in a new class — delegate to the mixin
or data structure.

## Step 2 — Missing but broadly useful → **SUGGEST, don't silently build**

If no existing infrastructure matches and you're about to
hand-roll the capability, apply the **rule of three + future
use** test. **Suggest** creating shared infrastructure when
ANY of these holds:

1. **≥3 existing classes** already hand-roll the same pattern
   (concrete duplication present today), OR
2. The capability is **foundational** (identity / equality /
   ordering / serialization / validation / event capture /
   container type) and will be reused by **≥2 concrete
   classes** current-or-imminent, OR
3. A **clean extraction point** exists in an adjacent module
   (e.g., the new class wants heap ops that belong in `f_ds`
   rather than the domain module).

**Do NOT create shared infrastructure when:**
- Only one class needs it AND the use case is narrow (YAGNI).
- The "infrastructure" is domain logic in disguise (it belongs
  in the domain module, not `f_core` / `f_ds`).

**How to suggest (mandatory script):** pause before writing
the new class and tell the user, using concrete file paths and
at least two naming examples:

> "I'm about to implement `<capability>` in `<new_class>`.
> `<existing_class_A>` and `<existing_class_B>` already
> hand-roll this. Propose extracting it into
> `f_core/<folder>/<name>.py` (or `f_ds/<folder>/<name>.py`)
> as a shared mixin/utility first. Proceed?"

**Wait for explicit confirmation.** Never silently extract —
new shared infrastructure is an architectural commitment the
user owns.

## Decision cheat-sheet

```
new class needed
    │
    ├── capability already in f_core/f_ds? ──► YES → use it (inherit/compose)
    │                                          │
    │                                          NO
    │                                          ▼
    ├── ≥3 hand-rolled duplicates OR foundational + ≥2 reusers?
    │       │
    │       ├── YES → SUGGEST new shared infra (wait for user OK)
    │       │
    │       └── NO  → write it inline in the new class (YAGNI)
```
