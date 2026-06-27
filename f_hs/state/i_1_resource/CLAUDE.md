# StateResource / NodeResource

## Purpose
Resource-Constrained search state for RCSPP. Lifts a node into the
**V×R product space** by making the state's identity the pair
`(node, resource)`, so the same node at different resource levels are
distinct states. This is the reduction that lets stock `AStar` /
`Dijkstra` solve RCSPP **unchanged** — single-label search over `(v, R)`
maintains one best-cost label per resource level (the non-dominated
frontier).

Two classes live here:
- **`NodeResource[Node]`** — the composite key value object (a
  `Tupleable`); `(node, resource)` is its identity. The type param is
  `Node` (the node's type), **not** `Key`: the *key* is the whole
  `NodeResource`, while `Node` is just its node component.
- **`StateResource[Node]`** — `StateBase` keyed on a `NodeResource`; adds
  `.node` / `.resource` sugar over the composite key.

`resource` is a discrete `int` (`R≥0`); discreteness is what keeps V×R
finite so the reduction terminates. `float` resources would break Tier 1
and require explicit label-dominance (Tier 2).

## Public API

### `NodeResource[Node]`
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

### `StateResource[Node]`
```python
def __init__(self, key: NodeResource[Node]) -> None
@property
def node(self) -> Key       # == key.node
@property
def resource(self) -> int   # == key.resource
```
`key` / `__eq__` / `__lt__` / `__hash__` / `__str__` come from `HasKey`
(delegating to the `NodeResource` key); `StateResource` adds no identity
overrides.

## Inheritance
```
Tupleable                         HasKey[Key]
   └── NodeResource[Node]           └── StateBase[Key]
       key = (node, resource)           ├── StateCell      (Key = CellMap)
                                        └── StateResource[Node]
                                            (Key = NodeResource[Node])
```
Note the layering: `StateBase`'s `Key` slot is filled by the **whole**
`NodeResource[Node]` (that IS the state's key); `Node` is only the node
*component* inside it.
`StateResource` is a flat sibling of `StateCell` under `StateBase`
(composition, **not** inheritance from `StateCell`): it composes the node
*key* into a `NodeResource`, generic over the node domain.

## Factory
| Method | Returns | Description |
|--------|---------|-------------|
| `at(row, col=None, resource=0)` | `StateResource` | At `(row, col)` (col defaults to row) with the given resource level |

## Dependencies
- `f_hs.state.StateBase` (aggregator) — identity base
- `f_core.mixins.Tupleable` (aggregator) — value-record identity for the key
- `f_ds.grids.CellMap` (aggregator, aliased `Cell`) — node key in the Factory

## Usage Example
```python
from f_hs.state import StateResource, NodeResource
from f_ds.grids import CellMap as Cell

# A node at resource level 3
state = StateResource(key=NodeResource(node=Cell(row=1, col=2), resource=3))
state.node       # CellMap(1, 2)
state.resource   # 3

# The V×R property: same cell, different resource → distinct states
a = StateResource.Factory.at(row=0, resource=3)
b = StateResource.Factory.at(row=0, resource=0)
a == b           # False
len({a, b})      # 2
```
