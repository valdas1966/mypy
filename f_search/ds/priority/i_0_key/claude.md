# i_0_key - PriorityKey

## Purpose
Base priority class that wraps a key and provides comparison via the `Comparable` mixin. Serves as the root of the priority inheritance hierarchy.

## Class: PriorityKey[Key]

### Attributes
- `_key: Key` - The identity key of the state (typically a grid cell or string)

### Methods
- `key_comparison() -> Key` - Returns the raw key for comparison
- `__repr__()` - String representation

### Comparison Semantics
Compares states purely by their key. This is the simplest form of ordering - lexicographic or natural order of the key type.

## Files
- `main.py` - `PriorityKey` class definition
- `__init__.py` - Re-exports `PriorityKey`

## Dependencies
- `f_core.mixins.Comparable` - Provides `<`, `>`, `==` operators via `key_comparison()`

## Role in Hierarchy
This is level 0 (base). All other priority classes inherit from this and extend the comparison tuple while preserving the key as the final tiebreaker.
