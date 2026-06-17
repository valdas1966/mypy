# Instruction to AI Agent (Claude Code): Import Conventions

## Aggregator vs Direct Imports — both first-class
Either form is fine; pick by ergonomics. They are equivalent in safety
and speed because aggregators are **lazy** (`ULazy`): `from f_pkg import X`
loads only `X`'s module on access, not its siblings — so it is just as
cascade-immune as a direct import (importing `Drive` won't fail if
`vertexai` for `Gemini` is broken).

```python
# Aggregator — ergonomic, groups related names
from f_gui.elements import Window, Container, Label
from f_core.mixins import Comparable

# Direct — addresses one leaf module explicitly
from f_google.services.drive import Drive
from f_search.algos.i_1_spp.i_1_astar import AStar
```

Aggregator packages MUST carry the `TYPE_CHECKING` mirror block (see
`__init__.py` Convention below) so the aggregator form resolves in IDEs /
mypy. All `ULazy` aggregators in the repo already have it.

## Import Order (PEP 8)
1. Standard library (`os`, `typing`, `abc`, `collections`)
2. Third-party (`pytest`, `loguru`, `google.auth`)
3. Framework (`f_core`, `f_ds`, `f_search`, `f_google`)

Separate groups with a blank line. Use absolute imports throughout.

## __init__.py Convention

Two types of `__init__.py` in this codebase:

**Leaf modules** — Factory wiring (eager imports):
```python
from f_class.main import MyClass
from f_class._factory import Factory

MyClass.Factory = Factory
```

**Aggregator packages** — lazy re-exports via `ULazy` + a
`TYPE_CHECKING` mirror block. `ULazy.install` wires the runtime
`__getattr__`/`__all__`/`__dir__`; the `if TYPE_CHECKING:` block (False
at runtime, so laziness is untouched; True for analyzers) makes the
names statically resolvable. Mirror each `module:attr` spec exactly.
```python
from typing import TYPE_CHECKING

from f_core.imports import ULazy

if TYPE_CHECKING:                        # analyzers only — never runs
    from f_pkg.sub_a import ClassA
    from f_pkg.sub_b import ClassB

ULazy.install(globals(), {
    'ClassA': 'f_pkg.sub_a:ClassA',
    'ClassB': 'f_pkg.sub_b:ClassB',
})
```
Lazy aggregators prevent cascade failures: importing one class
won't trigger loading all sibling packages. See
`f_core/imports/CLAUDE.md` for `ULazy` spec forms (symbol / module /
relative).

Never put business logic in `__init__.py`.
