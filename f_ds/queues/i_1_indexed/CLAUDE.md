# QueueIndexed

## Purpose
Indexed min-heap with decrease_key. Each item appears at most
once. Supports O(log n) push, pop, and decrease_key. Designed
for A* and Dijkstra where eager deletion replaces lazy deletion.

## Public API

### Constructor
```python
def __init__(self) -> None
```

### Methods
| Method | Signature | Description |
|--------|-----------|-------------|
| `push` | `(item, priority)` | Insert or decrease_key |
| `pop` | `-> Item` | Remove min-priority item |
| `peek` | `-> Item` | View min without removing |
| `decrease_key` | `(item, priority)` | Update if better |
| `clear` | `()` | Remove all items |
| `to_iterable` | `-> Iterable[Item]` | Items in priority order |
| `__contains__` | `(item) -> bool` | Membership check |
| `__len__` | `-> int` | Number of items |
| `__bool__` | `-> bool` | True if non-empty |

## Factory
| Method | Description |
|--------|-------------|
| `empty()` | Empty heap |
| `abc()` | A(3), B(1), C(2) — pops B, C, A |

## Design
- Priorities are tuples compared lexicographically
- push with existing item calls decrease_key
- decrease_key is a no-op if new priority is not better
- Pure Python — no C dependencies

## Dependencies
None (stdlib only).
