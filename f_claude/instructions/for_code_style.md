# Instruction to AI Agent: Code Style

## Type Annotations
- Annotate all function parameters and return types.
- Use `-> None` for methods that return nothing.
- Use modern union syntax: `type | None` (not `Optional`).
- Use lowercase generics: `dict[str, Any]`, `tuple[int, int]`,
  `list[str]`.
- Prefer `typing.Self` (PEP 673) over the literal class name when
  annotating the enclosing class's own instances:
  - **Returns** of fluent/`copy`/`classmethod`-constructor methods —
    `-> Self`.
  - **Same-type params** of domain/relationship methods — `other: Self`
    in `distance(self, other: Self) -> int`, `child: Self` in
    `add_child`, `parent: Self | None` in `__init__`.
  - **Exception**: comparison/equality dunders (`__lt__` … `__eq__`)
    keep `other: object`, not `Self` — they delegate to `key`.

```python
def __init__(self,
             row: int,
             col: int,
             name: str = 'CellBase') -> None:

@property
def key(self) -> tuple[int, int]:
```

## Clean Code: Decompose Complex Statements
Break a nested or complicated expression into a sequence of simple,
named statements. Each line does one thing; bind intermediate results to
descriptive locals instead of nesting a constructor/call inside another
call's argument.

```python
# Prefer — linear, each step named and inspectable
cell = Cell(row=0, col=0)
state = State(cell=cell)

# Over — a constructor nested inside another's argument
state = State(cell=Cell(row=0, col=0))
```

**Why:**
- Readable top-to-bottom; no inside-out parsing.
- Debuggable — print or breakpoint on `cell` before it is used;
  tracebacks point at the specific failing step.
- Named intermediates document intent and are easy to reuse/extend.

**Scope (do not over-apply):**
- The trigger is *nesting / complexity*, not single-use. Introducing a
  one-use local like `cell` above is correct because it un-nests a
  constructor argument.
- A single simple call needs no temporary — `len(items)`, `str(value)`,
  `f(x)` stay inline.
- Not anti-chaining: fluent/builder chains are a separate idiom and
  remain fine.
- Aim for *simple*, not *atomic* — don't shatter a clear expression into
  one token per line.

## Formatting
- **Indentation**: 4 spaces, no tabs.
- **Line length**: 80 characters.
- **Multi-line params**: align with opening parenthesis.
- **Blank lines**: 2 between top-level definitions, 1 between methods,
  none inside short methods.
- **Strings**: f-strings preferred —
  `f'{self.name}({self.row},{self.col})'`.
- **Named arguments** in calls:
  `data.set_best_to_be_parent_of(state=state)`.

## Class Definition Order
1. Class docstring
2. Class-level attributes (`Factory: type = None`, `cls_stats: type = ...`)
3. `__init__`
4. Properties (`@property`)
5. Public methods
6. Private methods (`_method`)
7. Dunder methods (`__str__`, `__repr__`, `__lt__`)
