# Instruction to AI Agent (Claude Code): Naming Conventions

## Folders
| Prefix | Meaning | Example |
|--------|---------|---------|
| `f_` | Framework module | `f_search`, `f_core`, `f_google` |
| `i_X_` | Inheritance level X | `i_0_base`, `i_1_astar`, `i_2_dijkstra` |
| `_internal/` | Private helper classes | `drive/_internal/` |
| (none) | Domain grouping | `algos/`, `problems/`, `solutions/`, `ds/` |

## Files
| Prefix | Meaning | Example |
|--------|---------|---------|
| `u_` | Utility module (functions, no classes) | `u_dict.py`, `u_file.py`, `u_datetime.py` |
| `c_` | Component / service wrapper | `c_loguru.py`, `c_timer.py` |
| `_` | Internal / private | `_factory.py`, `_tester.py` |
| (none) | Public module | `main.py` |

## Classes
- **PascalCase**: `AlgoSearch`, `CellBase`, `AStar`, `ProblemSPP`
- **Base classes**: named `*Base` or placed in `i_0_base/`
- **Mixins**: named as adjectives/capabilities — `Comparable`,
  `Printable`, `HasRowCol`, `ValidatableMutable`
- **Enums**: `TypeComparison`, `ServiceAccount`

## Functions and Methods
- **snake_case**: `_discover()`, `_handle_successor()`, `_need_relax()`
- **Private**: single `_` prefix — `_init_add_atts()`, `_pre_run()`
- **Factory statics**: short names for test objects — `a()`, `b()`,
  `gen()`
- **`_many` suffix (plural producer)**: a function/factory that returns
  several objects is suffixed `_many` and takes its count as a parameter
  named `many: int`; it returns a `list`. E.g.
  `random_many(grid, many, steps)` → `list[ClusterDiamond]`. The
  `many`↔`_many` pairing keeps the method/parameter relationship
  self-documenting across the codebase.

## Variables
- **Instance attributes**: `self._name` (single `_` for protected)
- **Local aliases**: short names in method bodies — `data = self._data`
- **Dict attributes**: descriptive prefixed names — `dict_g`, `dict_h`
- **Module-level constants**: `_UPPER_CASE` (private) — `_SCOPES = [...]`
- **Class-level constants**: `UPPER_CASE` (public) — `Factory: type = None`

## Type Variables
- PascalCase, descriptive, with bound:
```python
State = TypeVar('State', bound=StateBase)
Problem = TypeVar('Problem', bound=ProblemSearch)
Item = TypeVar('Item')
```
