# f_search - Heuristic Search on 2D Grids

## Project Overview
A comprehensive Python framework for implementing and researching heuristic search algorithms on grid-based maps. This project provides a clean, extensible architecture for solving pathfinding problems using classic search algorithms.

## Project Structure

### Core Components

- **algos/** - Search algorithm implementations (A*, Dijkstra, K×A*)
- **ds/** - Core data structures (State, Cost, Path, Generated queue)
- **problems/** - Problem definitions (SPP, OMSPP) with compositional mixins
- **solutions/** - Solution containers with paths and statistics
- **stats/** - Performance metrics and tracking
- **experiments/** - Research scripts for data generation and benchmarking

### Naming Convention

The project uses a hierarchical naming system with prefixes:

- **i_X_** prefix indicates inheritance/implementation level:
  - `i_0_base/` - Abstract base classes (level 0)
  - `i_1_xxx/` - First-level concrete implementations (level 1)
  - `i_2_xxx/` - Second-level specializations (level 2)

- **Problem type abbreviations:**
  - **SPP** - One-to-One Shortest Path Problem (single start, single goal)
  - **OMSPP** - One-to-Many Shortest Path Problem (single start, multiple goals)

### Architecture Pattern

The codebase follows a layered architecture:

```
Problem → Algorithm → Solution
   ↓          ↓          ↓
  Grid     Generated   Path
           Explored    Stats
           Cost
           State
```

**Data Flow:**
1. **Problem** defines the search space (grid, start, goal(s))
2. **Algorithm** searches using core data structures
3. **Solution** packages results (path(s), statistics)

## Design Patterns

### 1. Template Method Pattern
Algorithms define lifecycle hooks:
- `_run_pre()` - Initialize data structures
- `run()` - Execute main algorithm logic
- `_run_post()` - Calculate final statistics
- `_create_solution()` - Build solution object

### 2. Mixin Pattern
Problems compose functionality through mixins rather than deep inheritance:
- `HasStart` - Adds start state property
- `HasGoal` - Adds single goal state property
- `HasGoals` - Adds multiple goal states property

Example: `ProblemSPP(ProblemSearch, HasStart, HasGoal)`

### 3. Factory Pattern
Each major class includes a nested `Factory` class for creating test instances:
- `ProblemSPP.Factory.without_obstacles()`
- Enables easy testing and experimentation

### 4. Generic Type System
Heavy use of Python generics for type safety:
- `AlgoSearch[Problem, Solution]`
- `SolutionSearch[Stats]`
- `Cost[Key]`, `State[Key]`

## Key Classes

### Algorithm Hierarchy
```
AlgoSearch (Generic base)
  ├─ AlgoSPP (One-to-One base)
  │   ├─ AStar (A* with Manhattan heuristic)
  │   └─ Dijkstra (h=0, uninformed search)
  └─ AlgoOMSPP (One-to-Many base)
      └─ KxAStar (Naive K×A* approach)
```

### Problem Hierarchy
```
ProblemSearch (Grid-based base)
  ├─ ProblemSPP (Single start → Single goal)
  └─ ProblemOMSPP (Single start → Multiple goals)
```

### Data Structures
- **State**: Wraps a key (typically grid Cell) representing a search configuration
- **Cost**: Contains (g, h, key) with comparison via f=g+h
- **Path**: Sequence of states forming a solution path
- **Generated**: Dictionary-based priority queue (O(1) push, O(n) pop)

## Problem Types

### SPP (One-to-One Shortest Path Problem)
- **Definition**: Find shortest path from single start to single goal
- **Use Case**: Classic pathfinding (navigate A to B)
- **Algorithms**: AStar, Dijkstra

### OMSPP (One-to-Many Shortest Path Problem)
- **Definition**: Find shortest paths from single start to multiple goals
- **Use Case**: Visit multiple destinations from one source
- **Algorithms**: KxAStar (runs A* separately for each goal)

## External Dependencies

- **f_core** - Core utilities and mixins (Comparable, HasKey, etc.)
- **f_cs** - Computer science abstractions (Algo, ProblemAlgo)
- **f_ds** - Data structures (GridMap, CellMap, Dictable, Collectionable)

## Research Context

This framework supports research into:
- Heuristic search algorithm performance
- Multi-goal pathfinding strategies
- Grid-based navigation optimization
- Algorithm benchmarking and comparison

## Performance Tracking

Built-in statistics at every level:
- **GENERATED**: States added to open queue
- **UPDATED**: States re-added with better cost
- **EXPLORED**: States fully expanded
- **Elapsed time**: Algorithm execution duration
- **Per-goal metrics**: Individual statistics for OMSPP problems

## File Organization

Each module typically contains:
- `__init__.py` - Public exports
- `main.py` - Main class implementation
- `_factory.py` - Factory methods for testing (optional)
- `_tester.py` - Unit tests (optional)
- `_study.py` - Interactive exploration scripts (optional)
- `claude.md` - Documentation for Claude Code

Files with `_` prefix are private/internal.

## Key Features

1. **Clean Separation of Concerns**: Problem definition, algorithm logic, and results clearly separated
2. **Type Safety**: Strong typing with generics ensures compile-time checks
3. **Extensibility**: Easy to add new algorithms or problem types
4. **Testability**: Factory pattern and modular design enable easy testing
5. **Performance Metrics**: Comprehensive statistics tracking built-in
6. **Research-Ready**: Designed for algorithm comparison and experimentation
