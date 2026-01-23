# i_1_g - PriorityG

## Purpose
Priority class that orders states by their g-value (path cost from start). Higher g is preferred (negated in comparison), with key as tiebreaker.

## Class: PriorityG[Key] (extends PriorityKey)

### Attributes
- `_key: Key` (inherited)
- `_g: int` - Path cost from the start state

### Methods
- `update(g: int)` - Updates the g-value
- `key_comparison() -> tuple[int, Key]` - Returns `(-g, key)` so higher g gets higher priority
- `__repr__()` - String representation

### Comparison Semantics
Returns `(-g, key)`. The negation means states with higher g-values sort first. This is useful in search: among equal-f states, prefer deeper nodes (closer to the goal).

## Files
- `main.py` - `PriorityG` class definition
- `_factory.py` - Test instances: `a()` (g=0), `b()` (g=1), `c()` (g=1)
- `_tester.py` - Tests that b < a (g=1 beats g=0) and b < c (equal g, key tiebreaker)
- `__init__.py` - Re-exports and attaches Factory

## Dependencies
- `PriorityKey` from `i_0_key`

## Role in Hierarchy
Level 1. Used standalone for uninformed search (Dijkstra) where only g matters. Extended by `PriorityGH` to add heuristic.
