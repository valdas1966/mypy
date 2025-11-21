# ds - Data Structures for Search Algorithms

## Purpose
Contains core data structures used throughout the search framework. These classes provide the fundamental building blocks for representing states, costs, paths, and priority queues in grid-based pathfinding algorithms.

## Structure

- **state/** - `StateBase` - Represents a configuration in the search space
- **cost/** - `Cost` - Represents the cost/priority of reaching a state
- **path/** - `Path` - Represents a sequence of states forming a solution
- **generated/** - `Generated` - Priority queue for states awaiting exploration

## Core Concepts

### StateBase
**Purpose**: Wraps a key (typically a grid cell) to represent a search configuration

**Key Features:**
- Generic wrapper around a key type
- Provides semantic meaning (this is a "state" not just a "key")
- Used in sets and dictionaries for efficient lookup
- Identity determined by key equality

**Usage:**
- Start/goal states in problems
- Generated states in open queue
- Explored states in closed set
- Parent tracking in search tree
- Path representation in solutions

### Cost
**Purpose**: Represents the cost/priority of a state for ordering in priority queues

**Key Features:**
- Contains: g (path cost), h (heuristic), key (state reference)
- Supports: is_cached, is_bounded flags for advanced features
- Comparison via tuple: (f, !cached, !bounded, h, key)
  - f = g + h (total estimated cost)
  - Prioritizes non-cached over cached
  - Prioritizes non-bounded over bounded
  - Breaks ties with h-value, then key

**Usage:**
- Ordering states in Generated priority queue
- Determining which state to expand next
- Updating state priorities when better paths found

### Path
**Purpose**: Represents an ordered sequence of states from start to goal

**Key Features:**
- Wraps a list of StateBase objects
- Implements Collectionable (can convert to iterable)
- Implements Comparable (can compare paths)
- Provides: head(), tail(), reverse()
- Supports concatenation via + and += operators

**Usage:**
- Reconstructing solution paths from parent pointers
- Storing final solution paths
- Comparing paths for equality
- Combining path segments

### Generated
**Purpose**: Priority queue for states awaiting exploration (open list)

**Key Features:**
- Dictionary-based implementation (state → cost mapping)
- O(1) push operation (add/update state)
- O(n) pop operation (extract minimum cost state)
- Supports membership testing and updating
- Simple but effective for moderate-sized problems

**Usage:**
- Managing open states in search algorithms
- Retrieving next state to expand (lowest f-value)
- Updating state costs when better paths found
- Checking if state already generated

## Design Patterns

### Wrapper Pattern
StateBase and Path wrap simpler types (key, list) to provide semantic meaning and additional functionality.

### Generic Types
All data structures use Python generics for type safety:
- `StateBase[Key]`
- `Cost[Key]`
- `Path` (operates on `StateBase` objects)
- `Generated` (stores `StateBase` → `Cost` mappings)

### Mixin Composition
Classes implement standard interfaces:
- `HasKey` - Provides key access
- `Comparable` - Enables comparison operations
- `Collectionable` - Enables iteration
- `Dictable` - Dictionary-like interface

## Relationships

```
Search Algorithm
    ├─ Uses StateBase to represent configurations
    ├─ Uses Cost to prioritize states
    ├─ Uses Generated to manage open list
    └─ Uses Path to store solutions

StateBase ←─ wrapped by ─→ Cost (via key reference)
StateBase ←─ contained in ─→ Path (as sequence)
StateBase + Cost ←─ stored in ─→ Generated (as key-value pair)
```

## Performance Characteristics

| Data Structure | Operation | Complexity | Notes |
|----------------|-----------|------------|-------|
| **StateBase** | Create | O(1) | Simple wrapper |
| **StateBase** | Compare | O(1) | Via key equality |
| **Cost** | Create | O(1) | Stores g, h, key |
| **Cost** | Compare | O(1) | Tuple comparison |
| **Path** | Create | O(n) | Copies state list |
| **Path** | Reverse | O(n) | Creates new path |
| **Path** | Concatenate | O(n) | Combines lists |
| **Generated** | Push | O(1) | Dictionary insert |
| **Generated** | Pop | O(n) | Linear min search |
| **Generated** | Contains | O(1) | Dictionary lookup |

## External Dependencies

- **f_core.mixins** - Comparable, HasKey interfaces
- **f_ds.mixins** - Collectionable, Dictable interfaces
- **f_ds.grids** - GridMap, CellMap (for grid-based keys)

## Design Philosophy

### Simplicity
Each data structure has a focused responsibility:
- StateBase: Identity
- Cost: Priority
- Path: Sequence
- Generated: Queue

### Extensibility
Generic types allow different key types:
- Grid cells (typical)
- Indices
- Complex coordinates
- Custom state representations

### Composability
Data structures work together seamlessly:
- States go into Generated with Costs
- States come out of Generated for exploration
- States get assembled into Paths for solutions

## Trade-offs

### Generated Queue Implementation
**Current**: Dictionary-based with O(n) pop
- **Pros**: Simple, O(1) push/update, good for moderate n
- **Cons**: O(n) pop operation

**Alternative**: Heap-based with O(log n) pop
- **Pros**: O(log n) pop operation
- **Cons**: O(log n) update, more complex

**Design choice**: Simplicity over theoretical optimality for research framework

## Usage Example Flow

```
1. Create start state: state = StateBase(key=cell)
2. Calculate cost: cost = Cost(key=cell, g=0, h=heuristic)
3. Add to queue: generated.push(state, cost)
4. Get next state: state = generated.pop()
5. Explore state, generate successors, repeat
6. Reconstruct path: path = Path([state1, state2, ...])
```

## Relationship to Algorithms

All search algorithms depend on these data structures:
- **AlgoSearch** uses all four data structures
- **AStar/Dijkstra** populate Generated, extract States, build Paths
- **KxAStar** operates on Paths from multiple A* runs

## Key Invariants

1. **StateBase uniqueness**: States compared by key equality
2. **Cost consistency**: f = g + h always holds
3. **Path validity**: Paths contain connected state sequences
4. **Generated ordering**: Pop always returns minimum cost state
