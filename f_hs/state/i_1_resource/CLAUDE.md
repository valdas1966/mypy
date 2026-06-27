# StateResource / NodeResource

## Purpose
Resource-Constrained search state for RCSPP. Lifts a node into the
**V×R product space** by making the state's identity the pair
`(node, resource)`, so the same node at different resource levels are
distinct states. This is the reduction that lets stock `AStar` /
`Dijkstra` solve RCSPP **unchanged** — single-label search over `(v, R)`
maintains one best-cost label per resource level (the non-dominated
frontier).

Two names live here — one real class, one alias:
- **`NodeResource[Node]`** (real class) — the composite `(node, resource)`
  key value object (a `Tupleable`); `(node, resource)` is its identity.
  The type param is `Node` (the node's type), **not** `Key`: the *key* is
  the whole `NodeResource`, while `Node` is just its node component.
- **`StateResource[Node]`** (type alias) —
  `StateResource = StateBase[NodeResource[Node]]`. A search state keyed on
  a `NodeResource`. It is **not** a subclass: it carries no behavior, so
  per the codebase rule (behaviorless states use `StateBase[Key]`
  directly) it is a name, not a class.

```python
StateResource = StateBase[NodeResource[Node]]   # main.py (Node = TypeVar)
```

`resource` is a discrete `int` (`R≥0`); discreteness is what keeps V×R
finite so the reduction terminates. `float` resources would break Tier 1
and require explicit label-dominance (Tier 2).

Collapsed from a subclass to an alias on 2026-06-27 (alongside `StateCell`).
The old subclass added only `.node` / `.resource` sugar over the key; both
are read off the key instead (`state.key.node` / `state.key.resource`), so
the subclass was behaviorless and became an alias. `NodeResource` holds the
behavior.

## Public API

### `NodeResource[Node]` (the class)
```python
def __init__(self, node: Node, resource: int) -> None
@property
def node(self) -> Node                 # the underlying node identity
@property
def resource(self) -> int              # the resource level
def to_tuple(self) -> tuple[Node, int] # (node, resource) — the identity
```
`__eq__` / `__lt__` / `__hash__` / `__iter__` / `__getitem__` / `__len__`
/ `__str__` / `__repr__` all derive from `to_tuple()` via `Tupleable`.

### `StateResource[Node]` (the alias)
`StateResource(key=node_resource)` constructs a `StateBase` (the alias is
callable). `key` / `__eq__` / `__lt__` / `__hash__` / `__str__` come from
`StateBase` via `HasKey`, delegating to the `NodeResource` key.

- node component: `state.key.node`
- resource level: `state.key.resource`

## Inheritance
```
Tupleable                         HasKey[Key]
   └── NodeResource[Node]           └── StateBase[Key]
       key = (node, resource)           └── StateBase[NodeResource[Node]]
                                            (== StateResource alias)
```
Note the layering: `StateBase`'s `Key` slot is filled by the **whole**
`NodeResource[Node]` (that IS the state's key); `Node` is only the node
*component* inside it.

## Dependencies
- `f_hs.state.StateBase` (aggregator) — identity base
- `f_core.mixins.Tupleable` (aggregator) — value-record identity for the key
- `f_ds.grids.CellMap` (aggregator) — node key used in tests

## Usage Example
```python
from f_hs.state import StateResource, NodeResource
from f_ds.grids import CellMap as Cell

# A node at resource level 3
state = StateResource(key=NodeResource(node=Cell(row=1, col=2), resource=3))
state.key.node       # CellMap(1, 2)
state.key.resource   # 3

# The V×R property: same cell, different resource → distinct states
cell = Cell(row=0, col=0)
a = StateResource(key=NodeResource(node=cell, resource=3))
b = StateResource(key=NodeResource(node=cell, resource=0))
a == b           # False
len({a, b})      # 2
```
