# HasStarts - Mixin for Multiple Start States

## Main Class
`HasStarts`

## Purpose
Provides multiple start states property to problem classes. Mirrors
HasGoals but for start states. Used by ProblemMMSPP.

## Public API

### `__init__(self, starts: list[State]) -> None`
Store the list of start states.

### `starts -> list[State]` (property)
Return the list of start states. Read-only.

## Usage
```python
class ProblemMMSPP(ProblemSearch, HasStarts, HasGoals):
    def __init__(self, grid, starts, goals):
        ProblemSearch.__init__(self, grid=grid)
        HasStarts.__init__(self, starts=starts)
        HasGoals.__init__(self, goals=goals)
```
