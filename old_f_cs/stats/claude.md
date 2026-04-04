# StatsAlgo

## Purpose
Abstract base class for tracking algorithm execution statistics.
Provides an `elapsed` time property that subclasses extend with
algorithm-specific metrics.

## Public API

### `__init__(self, elapsed: int = 0) -> None`
Initialize with elapsed time (default 0).

### `elapsed -> int` (property, read/write)
Elapsed time in seconds. Getter and setter.

## Inheritance

```
StatsAlgo (root)
    └── StatsSearch, StatsSPP, StatsOMSPP, ...
```

No base classes — standalone root.

## Dependencies

None. Self-contained module.

## Usage Example

```python
from f_cs.stats import StatsAlgo

stats = StatsAlgo()
stats.elapsed = 42
print(stats.elapsed)  # 42
```
