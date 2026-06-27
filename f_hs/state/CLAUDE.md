# f_hs/state — Search States

## Purpose
State classes representing configurations in a search space.

## Module Structure
```
state/
├── __init__.py         StateBase, StateCell, StateResource, NodeResource
├── i_0_base/           StateBase[Key] — the only State class
├── i_1_cell/           StateCell = StateBase[CellMap]  (type alias)
└── i_1_resource/       StateResource = StateBase[NodeResource[Node]]  (alias)
                        + NodeResource — the (node, resource) key class
```

## The one-class rule
`StateBase[Key]` is the **only** State class. A State is pure identity, so
a behaviorless subclass is just a name — the codebase keys behaviorless
states on `StateBase[Key]` directly (`StateBase[str]` ~50×). `StateCell`
and `StateResource` are therefore **type aliases**, not subclasses
(collapsed 2026-06-27); the only real class besides `StateBase` is the key
value object `NodeResource`.

```
HasKey[Key]
  └── StateBase[Key]                          (the one State class)
        StateCell      = StateBase[CellMap]            (alias)
        StateResource  = StateBase[NodeResource[Node]] (alias)

Tupleable
  └── NodeResource[Node]   key = (node, resource); the V×R identity class
```

## RCSPP V×R reduction
`StateResource` keys on a `NodeResource` (node, resource) pair so the same
node at different resource levels are distinct states — the V×R reduction
that runs RCSPP on stock `AStar` / `Dijkstra`. `resource` is a discrete
`int` (`R≥0`), keeping V×R finite. `NodeResource` (a `Tupleable`) holds the
identity and the `.node` / `.resource` accessors; a state reads them off
its key (`state.key.node` / `state.key.resource`).
