# Naming Conventions - f_search Module

## Quick Reference for Claude Code

This document explains the naming patterns specific to the f_search module (heuristic search on 2D grids).

---

## Inheritance Hierarchy Visualization

### Complete Algorithm Hierarchy
```
AlgoSearch (algos/i_0_base)                    ← Level 0: Root algorithm base
├─ AlgoSPP (algos/i_1_spp/i_0_base)       ← Level 1: SPP base
│  ├─ AStar (algos/i_1_spp/i_1_astar)       ← Level 1: A* implementation
│  └─ Dijkstra (algos/i_1_spp/i_2_dijkstra) ← Level 2: Dijkstra (inherits AStar!)
└─ AlgoOMSPP (algos/i_1_omspp/i_0_base)       ← Level 1: OMSPP base
   └─ KxAStar (algos/i_1_omspp/i_1_kx_astar)  ← Level 1: K×A* implementation
```

**Key Insight**: Dijkstra is `i_2` because it inherits from AStar (i_1), not because it's worse or later!

### Complete Problem Hierarchy
```
ProblemSearch (problems/i_0_base)              ← Level 0: Grid search base
├─ ProblemSPP (problems/i_1_spp)          ← Level 1: One-to-One
└─ ProblemOMSPP (problems/i_1_omspp)          ← Level 1: One-to-Many
```

### Complete Solution Hierarchy
```
SolutionSearch (solutions/i_0_base)            ← Level 0: Base solution
├─ SolutionSPP (solutions/i_1_spp)        ← Level 1: SPP solution
└─ SolutionOMSPP (solutions/i_1_omspp)        ← Level 1: OMSPP solution
```

### Complete Stats Hierarchy
```
StatsSearch (stats/i_0_base)                   ← Level 0: Base statistics
├─ StatsSPP (stats/i_1_spp)               ← Level 1: SPP stats
└─ StatsOMSPP (stats/i_1_omspp)               ← Level 1: OMSPP stats (+ per-goal)
```

---

## Folder Structure Map

### Top Level
```
f_search/
├─ algos/           - Algorithm implementations
├─ ds/              - Data structures (StateBase, Cost, Path, Generated)
├─ problems/        - Problem definitions
├─ solutions/       - Solution containers
├─ stats/           - Performance statistics
└─ experiments/     - Research/benchmarking scripts
```

### algos/ Structure
```
algos/
├─ i_0_base/                      - AlgoSearch (root base class)
│  └─ main.py                     - Core search infrastructure
│
├─ i_1_spp/                     - One-to-One algorithms
│  ├─ i_0_base/                   - AlgoSPP base
│  ├─ i_1_astar/                  - A* algorithm
│  └─ i_2_dijkstra/               - Dijkstra (special case of A*)
│
└─ i_1_omspp/                     - One-to-Many algorithms
   ├─ i_0_base/                   - AlgoOMSPP base
   └─ i_1_kx_astar/               - K×A* (naive decomposition)
```

### problems/ Structure
```
problems/
├─ i_0_base/                      - ProblemSearch (grid base)
├─ i_1_spp/                     - ProblemSPP (start + goal)
├─ i_1_omspp/                     - ProblemOMSPP (start + goals)
└─ mixins/                        - Compositional mixins
   ├─ has_start/                  - HasStart mixin
   ├─ has_goal/                   - HasGoal mixin (singular)
   └─ has_goals/                  - HasGoals mixin (plural)
```

### ds/ Structure (No i_X hierarchy)
```
ds/
├─ state/           - StateBase (search configuration)
├─ cost/            - Cost (priority/f-value)
├─ path/            - Path (solution path)
└─ generated/       - Generated (priority queue)
```

**Note**: Data structures don't use `i_X` naming because they don't form deep inheritance hierarchies.

---

## Problem Type Conventions

### SPP (One-to-One Shortest Path Problem)
**Definition**: Single start → Single goal

**Naming pattern**: `*spp*` (lowercase in folders, PascalCase in classes)

**Components**:
- Problem: `ProblemSPP` (has start, goal)
- Algorithms: `AStar`, `Dijkstra`
- Solution: `SolutionSPP` (contains single path)
- Stats: `StatsSPP`

**Folder pattern**:
```
algos/i_1_spp/
problems/i_1_spp/
solutions/i_1_spp/
stats/i_1_spp/
```

### OMSPP (One-to-Many Shortest Path Problem)
**Definition**: Single start → Multiple goals

**Naming pattern**: `*omspp*` (lowercase in folders, PascalCase in classes)

**Components**:
- Problem: `ProblemOMSPP` (has start, goals)
- Algorithms: `KxAStar`
- Solution: `SolutionOMSPP` (contains dict of paths)
- Stats: `StatsOMSPP` (includes per-goal metrics)

**Folder pattern**:
```
algos/i_1_omspp/
problems/i_1_omspp/
solutions/i_1_omspp/
stats/i_1_omspp/
```

---

## Class Naming Patterns

### Algorithm Classes
- **Prefix**: `Algo` (e.g., `AlgoSearch`, `AlgoSPP`)
- **Suffix**: Problem type (e.g., `AlgoSPP`)
- **Specific**: Algorithm name (e.g., `AStar`, `Dijkstra`)

### Problem Classes
- **Prefix**: `Problem` (e.g., `ProblemSearch`, `ProblemSPP`)
- **Suffix**: Problem type (e.g., `ProblemSPP`)

### Solution Classes
- **Prefix**: `Solution` (e.g., `SolutionSearch`)
- **Suffix**: Problem type (e.g., `SolutionSPP`)

### Stats Classes
- **Prefix**: `Stats` (e.g., `StatsSearch`)
- **Suffix**: Problem type (e.g., `StatsSPP`)

### Data Structure Classes
- **Direct names**: `StateBase`, `Cost`, `Path`, `Generated`
- **No prefix/suffix**: These are fundamental building blocks

---

## Mixin Naming Pattern

### Pattern: `Has` + Feature

**Mixins** (problems/mixins/):
- `HasStart` - Adds `start` property (singular)
- `HasGoal` - Adds `goal` property (singular)
- `HasGoals` - Adds `goals` property (plural, set)

### Singular vs Plural
- **`HasGoal`**: Single goal → `problem.goal` returns `StateBase`
- **`HasGoals`**: Multiple goals → `problem.goals` returns `set[StateBase]`

### Usage Pattern
Problems compose mixins:
```python
ProblemSPP(ProblemSearch, HasStart, HasGoal)     # Singular goal
ProblemOMSPP(ProblemSearch, HasStart, HasGoals)    # Plural goals
```

---

## Special Naming Conventions

### Algorithm Variants

**KxAStar**: "K times A*"
- Runs A* algorithm K times (once per goal)
- `Kx` = "K times" (multiplicative)
- Naive decomposition approach

**Future examples**:
- `MultiGoalAStar` - Unified multi-goal search
- `IncrementalAStar` - Incremental search

### Nested i_X Folders

When you see nested inheritance levels:
```
algos/i_1_spp/i_2_dijkstra/
       ↑         ↑
       Level 1   Level 2 within SPP branch
```

**Reading**:
- First `i_1`: SPP is level 1 under AlgoSearch
- Second `i_2`: Dijkstra is level 2 under AlgoSPP (via AStar)

---

## File Naming Patterns

### Standard Files
- `main.py` - Main class implementation
- `__init__.py` - Public exports
- `claude.md` - Documentation for Claude Code

### Internal Files (underscore prefix)
- `_factory.py` - Factory methods for testing
- `_tester.py` - Unit tests
- `_study.py` - Exploratory scripts

### Experiments
- `pickle_grids.py` - Grid dataset generation
- `generate_cell_pairs.py` - Test case generation

---

## Data Structure Naming

### Core DS Classes
- `StateBase[Key]` - Wraps a key (grid cell)
- `Cost[Key]` - Priority/cost for state
- `Path` - Sequence of states
- `Generated` - Priority queue (open list)

**No i_X hierarchy**: These are foundational, not hierarchical.

---

## Import Patterns

### Typical Imports

```python
from f_search.algos import AStar, Dijkstra
from f_search.problems import ProblemSPP, ProblemOMSPP
from f_search.solutions import SolutionSPP, SolutionOMSPP
from f_search.stats import StatsSPP, StatsOMSPP
from f_search.ds import StateBase, Cost, Path, Generated
```

### Internal Imports (within f_search)
```python
from f_search.algos.i_0_base.main import AlgoSearch
from f_search.algos.i_1_spp.i_0_base.main import AlgoSPP
from f_search.algos.i_1_spp.i_1_astar.main import AStar
```

---

## Navigation Guide for Claude Code

### When Exploring a New Component

1. **Start with claude.md** - Read module overview
2. **Check i_0_base/** - Understand base abstraction
3. **Look at i_1_xxx/** - See main implementations
4. **Read main.py** - Study actual code

### When Tracing Inheritance

1. **Note folder depth** - Count i_X levels
2. **Read class definition** - Check base classes
3. **Cross-reference** - Match folder depth to class hierarchy

### When Understanding Relationships

1. **Check naming patterns** - SPP vs OMSPP
2. **Look for parallel structures** - algos, problems, solutions, stats
3. **Read claude.md comparisons** - Tables explain differences

---

## Common Patterns to Remember

### Pattern 1: Parallel Hierarchies
Problem type determines structure across all components:
```
SPP → ProblemSPP → AlgoSPP → SolutionSPP → StatsSPP
OMSPP → ProblemOMSPP → AlgoOMSPP → SolutionOMSPP → StatsOMSPP
```

### Pattern 2: Mixin Composition
Problems use mixins instead of deep inheritance:
```
Problem + HasStart + HasGoal  = SPP
Problem + HasStart + HasGoals = OMSPP
```

### Pattern 3: Specialization via Inheritance
Dijkstra extends AStar by overriding one method:
```
AStar (i_1)
  └─ Dijkstra (i_2) - just changes heuristic to 0
```

---

## Quick Lookup Table

| Abbreviation | Meaning | Example |
|--------------|---------|---------|
| SPP | One-to-One SPP | Single start → Single goal |
| OMSPP | One-to-Many SPP | Single start → Multiple goals |
| SPP | Shortest Path Problem | - |
| i_0 | Level 0 (base) | Abstract base class |
| i_1 | Level 1 | First-level implementation |
| i_2 | Level 2 | Second-level specialization |
| Algo | Algorithm | Class name prefix |
| Has | Mixin | HasStart, HasGoal, HasGoals |

---

## Tips for Claude Code

### When Asked About Hierarchy
- Use folder structure as primary source
- i_X number = inheritance depth
- Check claude.md for confirmation

### When Asked About Relationships
- SPP and OMSPP are siblings (different problem types)
- Parallel naming across algos/problems/solutions/stats
- Mixins provide compositional features

### When Asked About Implementation
- Base classes in i_0_base/
- Concrete implementations in i_1+
- Check main.py for actual code

### When Suggesting Changes
- Respect i_X hierarchy in naming
- Maintain parallel structure across components
- Follow established patterns (SPP/OMSPP style)
