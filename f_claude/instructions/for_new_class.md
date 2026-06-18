# Instruction to AI Agent (Claude Code): Writing New Code — Reuse-First Check

Before writing **any** new code (a class, a function, a utility, a
helper), run this **3-step check**. It is a pre-coding gate, same
category as *Clarify Before Acting*. The codebase's primary design
language is capability-as-mixin + reusable-data-structure — silently
re-implementing, forking, or working around existing code fragments the
framework (future migrations become N-site refactors).

**The three tiers, in order:**
1. It already exists and fits → **reuse it** (Step 1).
2. It exists but isn't good enough → **propose to improve it in place**
   (Step 2) — never silently fork, duplicate, or work around.
3. It doesn't exist and would help many tasks → **propose core/infra**
   (Step 3) — wait for OK; otherwise write it inline (YAGNI).

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

## Step 2 — Exists but not good enough → **propose to improve it**

If existing code *almost* fits but is missing a feature, has a bug, or
its API doesn't quite cover your case, do **not** silently fork it,
copy-paste a variant, or wrap it in a workaround. Improving the shared
code in place keeps the framework coherent and the fix benefits every
existing caller.

**How to propose (mandatory script):** name the existing code, the
gap, and the minimal change:

> "`<existing_class_or_util>` already does `<capability>` but lacks
> `<X>` / breaks on `<case>`. Propose improving it in place
> (`<file:path>`) by `<minimal change>`, rather than forking it.
> Proceed?"

**Wait for OK before any non-trivial change** to shared code — other
callers depend on it. A purely additive, backward-compatible tweak
(e.g. a new optional kwarg) can proceed with a one-line heads-up; a
behavior change to an existing path must wait for confirmation.

## Step 3 — Missing but broadly useful → **SUGGEST, don't silently build**

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
