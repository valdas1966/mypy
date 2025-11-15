# Naming Conventions - f_graph Module

## Quick Reference
Graph structures with node hierarchy using `i_X` naming.

---

## Node Hierarchy

### nodes/ - Node Inheritance
```
nodes/
├─ i_0_key/         - NodeKey (base: node with key/identifier)
└─ i_1_parent/      - NodeParent (adds parent pointer)
```

**Inheritance Chain**:
```
NodeKey (i_0)
  └─ NodeParent (i_1) - extends with parent tracking
```

**Purpose**:
- `NodeKey` - Basic node with identifier
- `NodeParent` - Node that tracks its parent (for tree traversal)

---

## Pattern

### i_0_key - Base Node
Foundation for all nodes:
- Provides key/identifier
- Basic node functionality

### i_1_parent - Extended Node
Specialization adding:
- Parent pointer
- Tree/hierarchy support
- Enables path reconstruction

---

## Design Rationale

**Why i_X here?**
- Clear inheritance relationship
- Parent extends Key with additional property
- Visual hierarchy in file structure

---

See `/mnt/g/mypy/NAMING_CONVENTION.md` for general conventions.
