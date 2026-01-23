# i_2_gh - PriorityGH

## Purpose
Priority class for informed search (A*). Orders states by f=g+h, breaking ties by maximizing g, then by key.

## Class: PriorityGH[Key] (extends PriorityG)

### Attributes
- `_key: Key` (inherited)
- `_g: int` (inherited) - Path cost from start
- `_h: int` - Heuristic estimate to goal

### Methods
- `update(g=None, h=None)` - Updates g and/or h (optional kwargs)
- `key_comparison() -> tuple[int, tuple[int, Key]]` - Returns `(g+h, (-g, key))`
- `__repr__()` - String representation

### Comparison Semantics
Returns `(g+h, PriorityG.key_comparison(self))` = `(f, (-g, key))`.
- Primary: minimize f = g + h (total estimated cost)
- Secondary: maximize g (prefer deeper nodes, closer to goal)
- Tertiary: key (deterministic tiebreaker)

## Files
- `main.py` - `PriorityGH` class definition
- `_factory.py` - Test instances: `a()` (g=1,h=2,f=3), `b()` (g=2,h=1,f=3), `c()` (g=1,h=3,f=4)
- `_tester.py` - Tests: b < a (equal f, b has higher g), a < c (lower f)
- `__init__.py` - Re-exports and attaches Factory

## Dependencies
- `PriorityG` from `i_1_g`

## Role in Hierarchy
Level 2. The standard priority for A* search. Extended by `PriorityGHFlags` to add cached/bounded flags.
