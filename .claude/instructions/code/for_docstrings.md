# Instruction to AI Agent (Claude Code): Docstring Conventions

## Separator Width Rule
The `=` count adjusts to keep total line width at 80 characters:
| Context | Indentation | `=` count |
|---------|-------------|-----------|
| Module-level | 0 spaces | 80 |
| Class docstring | 4 spaces | 76 |
| Method docstring | 8 spaces | 72 |

## Class Docstrings
```python
class AStar(Generic[State], AlgoSPP[State, DataHeuristics]):
    """
    ============================================================================
     AStar (A*) Algorithm.
    ============================================================================
    """
```

## Method Docstrings
```python
def _discover(self, state: State) -> None:
    """
    ========================================================================
     Discover the given State.
    ========================================================================
    """
```

## Inline Comments
Short, above the line they describe:
```python
# Aliases
data = self._data
# Set State's Parent
data.set_best_to_be_parent_of(state=state)
```
