# i_3_gh_flags - PriorityGHFlags

## Purpose
Priority class for advanced search variants that use caching and bounding. Extends GH by inserting `is_cached` and `is_bounded` flags into the comparison tuple between f-value and the g-tiebreaker.

## Class: PriorityGHFlags[Key] (extends PriorityGH)

### Attributes
- `_key: Key` (inherited)
- `_g: int` (inherited) - Path cost from start
- `_h: int` (inherited) - Heuristic estimate to goal
- `_is_cached: bool` - Whether this state's value is from a cache
- `_is_bounded: bool` - Whether this state's value is bounded

### Methods
- `key_comparison() -> tuple[int, bool, bool, tuple[int, Key]]` - Returns `(g+h, !cached, !bounded, (-g, key))`
- `__repr__()` - String representation

### Comparison Semantics
Returns `(g+h, not is_cached, not is_bounded, PriorityG.key_comparison(self))`.
- Primary: minimize f = g + h
- Secondary: prefer cached states (not cached = True sorts after False)
- Tertiary: prefer bounded states
- Quaternary: maximize g (via PriorityG, not PriorityGH)
- Final: key tiebreaker

Note: This class calls `PriorityG.key_comparison(self)` directly, bypassing `PriorityGH.key_comparison()`. This is intentional - it reconstructs the full tuple with flags inserted in the middle.

## Files
- `main.py` - `PriorityGHFlags` class definition
- `_factory.py` - Test instances: `cached()`, `bounded()`, `regular()` (all with same g=1,h=2)
- `_tester.py` - Tests ordering: cached < bounded < regular
- `__init__.py` - Re-exports and attaches Factory

## Dependencies
- `PriorityGH` from `i_2_gh`
- `PriorityG` from `i_1_g` (for key_comparison bypass)

## Role in Hierarchy
Level 3. The most specialized priority, used in search algorithms that cache heuristic values or use bounded suboptimality (e.g., weighted A*, focal search).
