# Naming Conventions - f_hs Module

## Quick Reference
Heuristic search module (possibly older or alternative to f_search) with node hierarchy.

---

## Node Hierarchy

### ds/nodes/ - Node Inheritance Chain
```
nodes/
├─ (i_0_base likely exists or nodes start at i_1)
├─ i_1_cost/        - NodeCost (node with cost/priority)
└─ i_2_flags/       - NodeFlags (adds boolean flags)
```

**Inheritance Chain** (inferred):
```
NodeBase (i_0)
  └─ NodeCost (i_1) - adds cost/priority
      └─ NodeFlags (i_2) - adds flags (visited, cached, etc.)
```

**Purpose**:
- Progressive enhancement of node capabilities
- Each level adds specific features
- Three-level hierarchy for search nodes

---

## Interpretation

### i_1_cost - Cost Extension
Adds to base node:
- Cost/priority value
- f-value, g-value, h-value
- Priority queue ordering

### i_2_flags - Flags Extension
Further extends with:
- Boolean state flags
- Visited/unvisited
- Cached/fresh
- Other status indicators

---

## Relationship to f_search

**Note**: This might be:
- Earlier version of search framework
- Alternative implementation
- Specialized variant

Compare with `f_search/ds/` which has:
- `StateBase` (simpler, no deep hierarchy)
- `Cost` (separate class, not node attribute)

---

See `/mnt/g/mypy/NAMING_CONVENTION.md` for general conventions.
