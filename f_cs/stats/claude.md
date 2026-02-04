# StatsAlgo Module

## Overview

**Location:** `f_cs/stats/main.py`

**Purpose:** Abstract base class for tracking algorithm execution statistics, primarily elapsed time.

| Aspect | Details |
|--------|---------|
| Class | `StatsAlgo` |
| Package | `f_cs.stats` |
| Export | `from f_cs.stats import StatsAlgo` |

## Architecture

```
┌─────────────────────────────────────┐
│           StatsAlgo                 │
├─────────────────────────────────────┤
│  _elapsed: int                      │
├─────────────────────────────────────┤
│  + elapsed (property)               │
│  + elapsed.setter                   │
└─────────────────────────────────────┘
```

## Components

### StatsAlgo

Base class for algorithm statistics tracking.

**Constructor:**
```python
def __init__(self, elapsed: int = 0) -> None
```

**Properties:**

| Property | Type | Description |
|----------|------|-------------|
| `elapsed` | `int` | Elapsed time in seconds (read/write) |

## Usage Examples

```python
from f_cs.stats import StatsAlgo

# Create stats instance
stats = StatsAlgo()

# Set elapsed time after algorithm runs
stats.elapsed = 42

# Read elapsed time
print(stats.elapsed)  # 42
```

## Inheritance Hierarchy

```
StatsAlgo
    │
    └── (subclasses for specific algorithm stats)
```

## Design Patterns

| Pattern | Usage |
|---------|-------|
| Base Class | Provides foundation for algorithm-specific stats |
| Property Pattern | Encapsulates _elapsed with getter/setter |

## Dependencies

| Dependency | Purpose |
|------------|---------|
| None | Self-contained module |
