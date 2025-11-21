# Path - Sequence of States in Search Space

## Main Class
`Path(Collectionable[StateBase], Comparable)`

## Inheritance
- **Base Classes:**
  - `Collectionable[StateBase]` (from f_ds.mixins.collectionable)
  - `Comparable` (from f_core.mixins.comparable)

## Purpose
Represents an ordered sequence of states forming a path through the search space. In grid-based pathfinding, a Path represents the solution: a sequence of states from start to goal that defines the route to follow.

## Core Functionality

### Constructor (`__init__`)
Creates a Path from an iterable of states.

**Parameters:**
- **states**: `Iterable[StateBase]` (optional) - Initial sequence of states
  - If provided: Converted to list and stored
  - If None: Empty list created

**Storage:**
- `_states`: Internal list of StateBase objects

**Examples:**
```python
path1 = Path()  # Empty path
path2 = Path([state1, state2, state3])  # Path with 3 states
```

### Collection Interface

#### `to_iterable()` → `list[StateBase]`
Converts the Path to a list of States (implements Collectionable interface).

**Returns:** The internal `_states` list

**Usage:** Enables iteration and access to underlying state sequence

### Path Access Methods

#### `head()` → `StateBase`
Returns the first state in the path (start of path).

**Returns:** `_states[0]`

**Usage:** Get the starting state of a path

**Note:** Will raise IndexError if path is empty

#### `tail()` → `StateBase`
Returns the last state in the path (end of path).

**Returns:** `_states[-1]`

**Usage:** Get the ending state of a path (typically the goal)

**Note:** Will raise IndexError if path is empty

#### `reverse()` → `Path`
Creates a reversed copy of the path.

**Returns:** New `Path` object with states in reverse order

**Implementation:** Uses Python's `reversed()` on the state list

**Usage:**
- Reconstructing paths built backwards (from goal to start)
- Creating return paths
- Bidirectional search

**Note:** Returns a NEW path object (immutable operation)

### Comparison Method

#### `key_comparison()` → `list[StateBase]`
Returns the state list for comparison (implements Comparable interface).

**Returns:** The internal `_states` list

**Usage:** Enables path comparison via state sequence equality

**Comparison Logic:**
- Paths compared by state sequences
- Two paths equal if they have same states in same order
- Lexicographic comparison for ordering

### Path Concatenation

#### `__add__(other: Path)` → `Path`
Concatenates two paths into a new path.

**Parameters:**
- **other**: Another Path object to append

**Returns:** New `Path` with combined state sequences

**Implementation:** Creates new path from `self._states + other._states`

**Usage:**
```python
path1 = Path([s1, s2, s3])
path2 = Path([s4, s5])
path3 = path1 + path2  # Path([s1, s2, s3, s4, s5])
```

**Note:** Creates a NEW path object (non-destructive)

#### `__iadd__(other: Path)` → `Path`
Appends another path to this path (in-place).

**Parameters:**
- **other**: Another Path object to append

**Returns:** Modified self (for chaining)

**Implementation:** Extends `_states` with `other._states`

**Usage:**
```python
path1 = Path([s1, s2, s3])
path2 = Path([s4, s5])
path1 += path2  # path1 now contains [s1, s2, s3, s4, s5]
```

**Note:** Modifies the path object in-place (destructive)

## Design Philosophy

### Wrapper Pattern
Path wraps a simple list of States:
- Provides semantic meaning (this is a "path" not just a "list")
- Enables future extension (add path properties, validation, etc.)
- Clean interface for path operations

### Immutability (Partial)
Some operations create new paths:
- `reverse()` → new path
- `+` → new path

Others modify in-place:
- `+=` → modifies self

This hybrid approach balances efficiency and safety.

### Type Safety
Path is specialized for StateBase objects:
- Type-safe operations
- Clear domain semantics
- Prevents mixing with other sequences

## Usage in Search Algorithms

### Path Reconstruction (AStar/Dijkstra)
```python
def _reconstruct_path(self) -> list[Path]:
    """Trace path from goal back to start using parent pointers"""
    states = []
    current = self._best  # Goal state

    while current is not None:
        states.append(current)
        current = self._parent.get(current)

    # Reverse because we built backwards
    path = Path(states).reverse()
    return [path]
```

### Multi-Path Solutions (OMSPP)
```python
paths = {}
for goal in goals:
    path = reconstruct_path_to(goal)
    paths[goal] = path

solution = SolutionOMSPP(paths=paths)
```

### Path Combination
```python
# Combine path segments
segment1 = Path([s1, s2, s3])
segment2 = Path([s3, s4, s5])  # Note: s3 appears in both
full_path = segment1 + segment2  # May need to remove duplicate s3
```

## Relationship to Other Classes

- **StateBase**: Path contains ordered sequence of States
- **Solution**: Solutions contain Paths as results
  - `SolutionSPP`: Single Path
  - `SolutionOMSPP`: Multiple Paths (dict[StateBase, Path])
- **Algorithms**: Construct Paths during solution creation

## Properties

### Sequence Properties
- **Ordered**: States appear in specific order
- **Connected**: Adjacent states should be neighbors (by convention)
- **Non-empty** (typically): Valid solution paths contain at least start state

### Length
Path length can be computed as:
```python
len(path.to_iterable())  # Number of states
len(path.to_iterable()) - 1  # Number of edges/steps
```

## Performance

| Operation | Complexity | Notes |
|-----------|------------|-------|
| Create | O(n) | Copies state list |
| to_iterable | O(1) | Returns reference |
| head/tail | O(1) | Direct access |
| reverse | O(n) | Creates new path |
| + concat | O(n+m) | Creates new path |
| += append | O(m) | Extends list |
| Comparison | O(n) | Compares state sequences |

## Class Attribute
- **Factory**: Type reference for factory pattern (set in `__init__.py`)

## Common Patterns

### Empty Path Check
```python
path = Path()
if not path.to_iterable():
    # Path is empty
```

### Path Length
```python
num_states = len(path.to_iterable())
num_steps = num_states - 1
```

### Iterate States
```python
for state in path.to_iterable():
    # Process each state
```

### Build Path Incrementally
```python
path = Path()
path += Path([state1])
path += Path([state2])
path += Path([state3])
```

### Reverse Path
```python
forward_path = Path([s1, s2, s3])
backward_path = forward_path.reverse()  # Path([s3, s2, s1])
```

## Validation Considerations

While not enforced by the class, valid solution paths should satisfy:
1. **Connectivity**: Adjacent states are neighbors in the grid
2. **Start/Goal**: Path begins at start state, ends at goal state
3. **Non-empty**: Contains at least the start state
4. **No cycles** (typically): States don't repeat (shortest path)

These properties are ensured by the algorithm logic, not by the Path class itself.

## Example Usage

```python
# Reconstruct path from parent pointers
states = [start]
current = start

while current != goal:
    current = successors[current]
    states.append(current)

path = Path(states)

# Access endpoints
print(f"Start: {path.head()}")  # start
print(f"Goal: {path.tail()}")   # goal

# Reverse for backward traversal
return_path = path.reverse()

# Combine with another segment
extended = path + Path([next_state])
```
