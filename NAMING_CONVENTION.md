# Naming Conventions - g:\mypy Codebase

## Overview
This codebase uses consistent naming patterns to indicate structure, relationships, and purpose. Understanding these conventions is essential for navigating the code efficiently.

---

## 1. Module Naming: `f_` Prefix

### Pattern
All top-level modules use the `f_` prefix:
```
f_search/      - Heuristic search algorithms
f_ds/          - Data structures
f_core/        - Core utilities and mixins
f_cs/          - Computer science abstractions
f_graph/       - Graph structures and algorithms
f_math/        - Mathematical utilities
f_ai/          - AI/ML related code
...
```

### Purpose
- **Namespace organization**: Groups related functionality
- **Import clarity**: `from f_search import ...` is self-documenting
- **Collision avoidance**: Prevents name conflicts with standard library
- **Visual grouping**: Modules sort together in file browsers

### Meaning of 'f'
Likely stands for "Framework" - provides consistent prefix across all custom modules.

---

## 2. Inheritance Hierarchy: `i_X_` Prefix

### Pattern
Folders use `i_X_name` where:
- `i` = "inheritance" or "implementation level"
- `X` = depth in inheritance hierarchy (0, 1, 2, ...)
- `name` = descriptive identifier

### Hierarchy Levels

#### `i_0_base` - Abstract Base Classes
- Level 0 in the inheritance hierarchy
- Contains abstract/base classes
- Provides foundational structure and interface
- Not meant for direct instantiation

#### `i_1_xxx` - First-Level Implementations
- Level 1: Direct children of i_0 base classes
- Concrete implementations or specialized abstractions
- May still be abstract if further specialization needed

#### `i_2_xxx` - Second-Level Specializations
- Level 2: Children of i_1 classes
- Further specializations or variants
- Often concrete implementations with specific behavior

#### `i_N_xxx` - Deeper Hierarchies
- Level N: Continues for deeper inheritance trees
- Rare but used when needed

### Examples

#### f_search/algos - Algorithm Hierarchy
```
algos/
├─ i_0_base/                    AlgoSearch (abstract base)
├─ i_1_oospp/                   One-to-One algorithms
│  ├─ i_0_base/                 AlgoOOSPP (OOSPP base)
│  ├─ i_1_astar/                AStar (concrete)
│  └─ i_2_dijkstra/             Dijkstra (inherits from AStar!)
└─ i_1_omspp/                   One-to-Many algorithms
   ├─ i_0_base/                 AlgoOMSPP (OMSPP base)
   └─ i_1_kx_astar/             KxAStar (concrete)
```

**Inheritance Chain:**
```
AlgoSearch (i_0_base)
  └─ AlgoOOSPP (i_1_oospp/i_0_base)
      └─ AStar (i_1_oospp/i_1_astar)
          └─ Dijkstra (i_1_oospp/i_2_dijkstra)
```

#### f_ds/grids/cell - Cell Hierarchy
```
cell/
├─ i_0_base/                    Cell (base)
└─ i_1_map/                     CellMap (map-specific cell)
```

#### f_graph/nodes - Node Hierarchy
```
nodes/
├─ i_0_key/                     NodeKey (base with key)
└─ i_1_parent/                  NodeParent (adds parent pointer)
```

### Sibling Disambiguation

When multiple `i_1_xxx` folders exist at the same level:
```
algos/
├─ i_1_oospp/      ← Sibling branch (One-to-One)
└─ i_1_omspp/      ← Sibling branch (One-to-Many)
```

These are **sibling branches**, not alternatives:
- Both inherit from the same parent (i_0_base)
- Serve different purposes (different problem types)
- Number doesn't indicate preference or order
- Number after i_1 can be semantic (oospp vs omspp) or sequential

### Benefits

1. **Visual Hierarchy**: See inheritance depth at a glance
2. **Natural Sorting**: Folders sort by depth (base classes first)
3. **Searchability**: Easy to find all level-N implementations
4. **Refactoring Aid**: Inheritance changes are visible in structure
5. **Documentation**: File browser shows class relationships

### Reading Guide

When exploring a module with `i_X` folders:

1. **Start with i_0_base**: Understand the base abstraction
2. **Check i_1_xxx**: See main implementations/specializations
3. **Look at i_2_xxx**: Find further refinements
4. **Count levels**: Depth indicates inheritance distance from base

---

## 3. Internal Files: `_` Prefix

### Pattern
Files starting with underscore are internal/private:
```
_factory.py      - Factory methods for testing
_tester.py       - Unit tests
_study.py        - Exploratory/research scripts
```

### Purpose
- **Privacy signal**: Not part of public API
- **Organization**: Separate implementation from interface
- **Testing/Research**: Development utilities

---

## 4. Problem Type Abbreviations

### Common Abbreviations

**OOSPP** - One-to-One Shortest Path Problem
- Single start → Single goal
- Classic pathfinding

**OMSPP** - One-to-Many Shortest Path Problem
- Single start → Multiple goals
- Multi-destination routing

**Future possibilities:**
- MOSPP: Many-to-One
- MMSPP: Many-to-Many

### Usage
These appear in folder names, class names, and documentation:
```
problems/i_1_oospp/         - OOSPP problem definition
algos/i_1_oospp/            - OOSPP algorithms
solutions/i_1_oospp/        - OOSPP solutions
stats/i_1_oospp/            - OOSPP statistics
```

---

## 5. File Organization Pattern

### Typical Module Structure
```
module_name/
├─ __init__.py              - Public exports
├─ main.py                  - Main class implementation
├─ _factory.py              - Factory methods (optional)
├─ _tester.py               - Tests (optional)
├─ _study.py                - Research scripts (optional)
└─ claude.md                - Documentation for Claude Code
```

### Special Files

**claude.md** - Documentation for AI code assistant
- Explains module purpose and structure
- Details class functionality
- Shows usage examples
- Not traditional code documentation

**NAMING_CONVENTION.md** (this file)
- Explains naming patterns
- Helps navigate the codebase
- Reference for understanding structure

---

## Quick Reference

### Identify Class Level
```
i_0_*     → Abstract base class
i_1_*     → First-level implementation
i_2_*     → Second-level specialization
i_N_*     → N-th level in hierarchy
```

### Identify Module Type
```
f_*       → Framework module
i_*       → Inheritance level
_*        → Internal/private
```

### Identify Problem Type
```
*oospp*   → One-to-One pathfinding
*omspp*   → One-to-Many pathfinding
```

---

## Navigation Tips

### Finding Base Classes
1. Look for `i_0_base/` folders
2. Check `main.py` inside for abstract base class

### Understanding Inheritance
1. Note the `i_X` number in folder path
2. Higher X = deeper in inheritance tree
3. Check claude.md for inheritance diagram

### Tracing Hierarchy
1. Start at i_0_base
2. Follow i_1, i_2, etc. to see specializations
3. Use folder structure as visual inheritance tree

---

## Conventions by Module

See module-specific NAMING_CONVENTION.md files in:
- `f_search/NAMING_CONVENTION.md` - Detailed search algorithm conventions
- Other modules as needed

---

## Philosophy

These conventions support:
- **Research workflows**: Clear algorithm relationships
- **Code navigation**: Visual hierarchy in file browser
- **Type safety**: Inheritance patterns clear from structure
- **Maintainability**: Refactoring visible in file organization
- **Documentation**: Self-documenting file structure

When in doubt, the `i_X` number indicates inheritance depth, not preference or quality.
