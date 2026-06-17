# Instruction to AI Agent (Claude Code): Module Structure & Layout

How modules and class folders are organized in the MyPy framework. Read
this when scaffolding a new module/folder or navigating the hierarchy.

## Top-Level Modules
Framework modules use the `f_` prefix: `f_core`, `f_ds`, `f_search`, `f_google`, `f_utils`, `f_gui`, `f_cs`, etc.

## Module Internal Hierarchy
Modules use `i_X_name/` folders to express inheritance depth:
```
f_search/algos/
├── i_0_base/i_0_search/        # Level 0 — abstract root (AlgoSearch)
├── i_1_spp/                    # Level 1 — SPP family
│   ├── i_0_base/               # Level 1→0 — abstract SPP base
│   ├── i_1_astar/              # Level 1→1 — AStar
│   └── i_2_dijkstra/           # Level 1→2 — Dijkstra (extends AStar)
└── i_2_omspp/                  # Level 2 — One-to-Many family
```
The number after `i_` indicates the inheritance level within that scope. `i_0_` is always the abstract base.

## Standard Files Per Module
Every class module contains a subset of these files:
| File | Required | Purpose |
|------|----------|---------|
| `main.py` | Yes | Primary class implementation |
| `__init__.py` | Yes | Public exports; wires `Factory` onto the class |
| `_factory.py` | If testable | Factory class for creating common instances |
| `_tester.py` | If testable | pytest unit tests |
| `_study.py` | No | Exploratory / research scripts |
| `_run_tests.py` | No | Batch runner for all `_tester.py` in subtree |
| `_from.py` | No | Static constructors from external formats |
| `_to.py` | No | Instance conversion methods to external formats |
| `CLAUDE.md` | Yes | Module-specific docs for Claude Code |
| `CLAUDE.html` | On demand | Dark-themed HTML docs with TOC/search |
| `CLAUDE_REVIEW.html` | On demand | Code + design review (10 sections) |
| `ABOUT.html` | On demand | Visual overview for human reading |

Files prefixed with `_` are internal/private and not imported externally.
