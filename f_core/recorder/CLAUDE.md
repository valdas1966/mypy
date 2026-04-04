# Recorder

## Purpose
Structured event recorder for analysis. Records events as dicts
into an in-memory list. Opt-in via `is_active` flag — zero cost
when inactive. Designed for composition into ProcessBase, Algo,
and Solution objects.

## Public API

### Constructor
```python
def __init__(self, is_active: bool = False) -> None
```

### Properties
| Property | Type | Access | Description |
|----------|------|--------|-------------|
| `is_active` | `bool` | R/W | Whether recording is enabled |
| `events` | `list[dict]` | R | Copy of recorded events |

### Methods
| Method | Description |
|--------|-------------|
| `record(event: dict)` | Append event (no-op when inactive) |
| `clear()` | Remove all recorded events |
| `to_dataframe()` | Return events as pandas DataFrame |
| `__len__()` | Number of recorded events |
| `__bool__()` | True if recorder is active |

## Inheritance
Standalone class. No base classes.

## Dependencies
- `pandas` (lazy import in `to_dataframe()` only)

## Usage
```python
from f_core.recorder import Recorder

recorder = Recorder(is_active=True)
recorder.record({'type': 'discover', 'state': (0, 0), 'g': 0})
recorder.record({'type': 'explore', 'state': (0, 0)})
print(len(recorder))       # 2
df = recorder.to_dataframe()
```
