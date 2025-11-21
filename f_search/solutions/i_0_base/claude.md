# SolutionSearch - Base Solution for Search Problems

## Main Class
`SolutionSearch[Stats](Generic[Stats], SolutionAlgo[Stats])`

## Inheritance
- **Base Classes:**
  - `Generic[Stats]` - Generic type parameter
  - `SolutionAlgo[Stats]` - Generic solution interface from f_cs

- **Type Parameter:**
  - `Stats` bounded to `StatsSearch`

## Purpose
Provides the foundational structure for all search algorithm solutions. Defines the core components that every solution must have: validity status and performance statistics.

## Functionality from Base Classes

### From SolutionAlgo
- Generic solution interface
- Solution lifecycle management
- Base structure for algorithm results

## Specialized Functionality

### Constructor (`__init__`)
**Parameters:**
- **is_valid**: `bool` - Whether the solution is valid (goal(s) reached)
- **stats**: `Stats` - Statistics object tracking performance

**Implementation:**
```python
SolutionAlgo.__init__(self, is_valid=is_valid, stats=stats)
```

**Initializes:**
1. Validity flag (via SolutionAlgo)
2. Statistics object (via SolutionAlgo)

## Core Components

### Validity Flag (`is_valid`)
**Type:** `bool`

**Meaning:**
- `True`: Algorithm succeeded, goal(s) reached
- `False`: Algorithm failed, no valid path found

**Inherited from:** SolutionAlgo

**Usage:**
```python
if solution.is_valid:
    # Process successful solution
else:
    # Handle failure
```

### Statistics Object (`stats`)
**Type:** `Stats` (generic, bounded to `StatsSearch`)

**Contains:** Performance metrics from algorithm execution

**Inherited from:** SolutionAlgo

**Usage:**
```python
print(f"Generated: {solution.stats.generated}")
print(f"Explored: {solution.stats.explored}")
print(f"Time: {solution.stats.elapsed}s")
```

## Generic Type System

### Type Parameter: Stats
Bounded to `StatsSearch`, allows specialization:
- `SolutionSPP` uses `StatsSPP`
- `SolutionOMSPP` uses `StatsOMSPP`
- Future solutions can use custom stats

**Benefits:**
- Type safety: Correct stats type guaranteed
- Flexibility: Different problems can have different stats
- Extensibility: Easy to add new stats types

## Template for Specialization

SolutionSearch provides minimal base:
- Validity flag
- Statistics object
- Nothing more

Subclasses add problem-specific components:
- SPP: adds `path` (single Path)
- OMSPP: adds `paths` (dict[StateBase, Path])

## Design Philosophy

### Minimal Base Class
Provides only essential components:
- Is the solution valid?
- What were the performance metrics?

Leaves path/result structure to subclasses.

### Separation of Concerns
- **SolutionSearch**: Validity + Statistics (generic)
- **SolutionSPP**: + Single path (SPP-specific)
- **SolutionOMSPP**: + Multiple paths (OMSPP-specific)

### Immutability
Solutions are immutable after creation:
- Represents final algorithm result
- No methods to modify validity or stats
- Safe to share and cache

## Relationship to Other Classes

- **SolutionAlgo**: Base interface (from f_cs)
- **StatsSearch**: Statistics base class
- **SolutionSPP/OMSPP**: Concrete solution types
- **Algorithms**: Produce solutions

## Usage Context

- **Direct instantiation**: Not typical (too generic, no paths)
- **Specialization**: Extended by SolutionSPP, SolutionOMSPP
- **Role in hierarchy**: Root solution class for search problems

## Extension Pattern

To create a new solution type:

```python
class SolutionNewType(SolutionSearch[StatsNewType]):
    def __init__(self, is_valid, stats, additional_data):
        SolutionSearch.__init__(self, is_valid=is_valid, stats=stats)
        self._additional_data = additional_data

    @property
    def additional_data(self):
        return self._additional_data
```

## Key Properties

1. **Generic base**: Works with any StatsSearch subclass
2. **Minimal interface**: Only validity and statistics
3. **Template pattern**: Subclasses add specific data
4. **Type safe**: Generic parameter ensures stats type correctness
5. **Immutable**: No modification after creation
