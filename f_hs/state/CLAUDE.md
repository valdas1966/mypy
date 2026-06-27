# f_hs/state — Search States

## Purpose
State classes representing configurations in a search space.

## Module Structure
```
state/
├── __init__.py         StateBase, StateCell, StateResource, NodeResource
├── i_0_base/           StateBase[Key] — generic base
├── i_1_cell/           StateCell — CellMap for 2D grids
└── i_1_resource/       StateResource — V×R state for RCSPP
                        (+ NodeResource key value object)
```

## Inheritance
```
HasKey[Key]
  └── StateBase[Key]
        ├── StateCell (Key=CellMap)
        └── StateResource[Node] (Key=NodeResource[Node])

Tupleable
  └── NodeResource[Node]   key = (node, resource); the V×R identity
```

`StateResource` is a flat sibling of `StateCell` (composition, not
inheritance): it keys on a `NodeResource` (node, resource) pair so the
same node at different resource levels are distinct states — the V×R
reduction that runs RCSPP on stock `AStar` / `Dijkstra`. `resource` is a
discrete `int` (`R≥0`), keeping V×R finite.
