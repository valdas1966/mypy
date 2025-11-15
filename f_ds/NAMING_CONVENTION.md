# Naming Conventions - f_ds Module

## Quick Reference
Data structures module with selective use of `i_X` hierarchy for classes with inheritance relationships.

---

## Modules with i_X Hierarchy

### grids/cell/ - Cell Hierarchy
```
cell/
├─ i_0_base/        - Cell (base cell class)
└─ i_1_map/         - CellMap (map-specific cell)
```

**Inheritance**: `Cell` → `CellMap`

### queues/ - Queue Hierarchy
```
queues/
├─ i_0_base/        - Base queue class
└─ i_1_priority/    - Priority queue implementation
```

**Inheritance**: `QueueBase` → `PriorityQueue`

---

## Modules WITHOUT i_X Hierarchy

Most data structures are standalone or shallow inheritance:

### Common DS (No hierarchy)
- `mixins/` - Reusable traits (Comparable, Collectionable, Dictable, etc.)
- `trees/` - Tree structures
- `graphs/` - Graph structures
- Other standalone data structures

**Reason**: These don't form deep inheritance hierarchies, so `i_X` naming not needed.

---

## Pattern Recognition

### Has i_X hierarchy → Multiple inheritance levels
Example: Cell has specialized CellMap variant

### No i_X hierarchy → Standalone or mixin-based
Example: Comparable is a mixin, not part of hierarchy

---

## Navigation Tips

1. **Check for i_X folders** - Indicates inheritance hierarchy
2. **No i_X** - Likely standalone classes or mixins
3. **Read main.py** - Understand class structure

---

See `/mnt/g/mypy/NAMING_CONVENTION.md` for general conventions.
