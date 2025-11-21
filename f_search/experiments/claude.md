# experiments - Research Scripts for Data Generation

## Purpose
Contains experimental scripts for generating test data and preparing benchmarks for heuristic search research. These scripts create pickled datasets for use in algorithm evaluation and comparison.

## Structure

- **pickle_grids.py** - Loads and pickles grid maps from files
- **generate_cell_pairs.py** - Generates test cell pairs for pathfinding benchmarks

## Scripts Overview

### pickle_grids.py
**Purpose**: Loads grid maps from files and saves them as pickled Python objects

**Workflow:**
1. Reads grid map files from `g:\paper\maps`
2. Groups maps by domain/category
3. Serializes maps using pickle
4. Saves to `g:\paper\grids.pkl`

**Use Case:**
- Prepare grid maps for experiments
- Create reusable dataset of maps
- Speed up repeated experiments (avoid re-parsing files)

**Output Format**: Pickled dictionary of grid maps

### generate_cell_pairs.py
**Purpose**: Generates random cell pairs for pathfinding benchmarks

**Workflow:**
1. Loads grids (likely from pickled file)
2. Generates 1,000,000 (1M) cell pairs
3. Ensures minimum Manhattan distance between pairs
4. Pairs represent start-goal combinations for testing
5. Saves to `g:\paper\pairs.pkl`

**Constraints:**
- Pairs have minimum separation (meaningful pathfinding problems)
- Cells are valid (on grid, not obstacles)
- Large dataset for statistical significance

**Use Case:**
- Create benchmark test cases
- Ensure diverse problem instances
- Enable reproducible experiments

**Output Format**: Pickled list/dict of cell pairs

## Research Workflow

### Typical Usage Pattern

1. **Setup** (one-time):
   ```bash
   # Generate grids dataset
   python experiments/pickle_grids.py
   # Output: g:\paper\grids.pkl

   # Generate test pairs
   python experiments/generate_cell_pairs.py
   # Output: g:\paper\pairs.pkl
   ```

2. **Experiments** (repeated):
   ```python
   import pickle

   # Load pre-generated data
   with open('g:/paper/grids.pkl', 'rb') as f:
       grids = pickle.load(f)

   with open('g:/paper/pairs.pkl', 'rb') as f:
       pairs = pickle.load(f)

   # Run algorithms on test cases
   for grid_name, grid in grids.items():
       for start_cell, goal_cell in pairs:
           problem = ProblemSPP(grid, StateBase(start_cell), StateBase(goal_cell))
           solution = algorithm.run(problem)
           # Collect results...
   ```

## Data Location

### Input
- **Grid maps**: `g:\paper\maps` (raw map files)

### Output
- **Pickled grids**: `g:\paper\grids.pkl`
- **Pickled pairs**: `g:\paper\pairs.pkl`

**Note:** Paths are Windows-specific (G: drive)

## File Organization

Both scripts are likely standalone executables:
- No `__init__.py` (not a package)
- Self-contained scripts
- Run directly with Python

## Pickle Format

**Advantages:**
- Fast serialization/deserialization
- Preserves Python object structure
- Native Python format
- Efficient for large datasets

**Disadvantages:**
- Not human-readable
- Python-specific (not portable to other languages)
- Security concerns (don't unpickle untrusted data)

## Research Context

These scripts support:
- **Algorithm benchmarking**: Consistent test cases
- **Reproducibility**: Same data across runs
- **Performance evaluation**: Large-scale testing
- **Algorithm comparison**: Fair evaluation on identical problems

## Typical Benchmark Setup

### Grid Map Sources
Maps likely come from standard benchmarks:
- Moving AI Lab benchmarks
- Game maps (Dragon Age, StarCraft, etc.)
- Random mazes
- Real-world scenarios

### Test Pair Characteristics
1M pairs provide:
- Statistical significance
- Coverage of problem space
- Various difficulty levels
- Diverse start-goal configurations

## Extension Opportunities

Potential additions:
- **pickle_problems.py**: Pre-generate ProblemSPP instances
- **generate_omspp_cases.py**: Multi-goal test cases
- **benchmark_runner.py**: Automated experiment execution
- **results_analyzer.py**: Statistical analysis of results

## Usage Considerations

### Storage Requirements
- Grids: Depends on map count and size
- 1M pairs: Modest storage (each pair is two coordinates)
- Pickle files: Binary format, compressed by Python

### Generation Time
- `pickle_grids.py`: Fast (I/O bound, file reading)
- `generate_cell_pairs.py`: Moderate (1M iterations with validation)

### Reproducibility
- Consider seeding random number generator
- Document generation parameters
- Version control for scripts
- Save metadata with pickled files

## Design Philosophy

### Separation of Concerns
- **Generation** (experiments): Create test data once
- **Execution** (main code): Use test data many times
- **Analysis** (separate): Process results

### Reusability
- Generate data once, use many times
- Share datasets across experiments
- Enable collaborative research

### Performance
- Avoid repeated file parsing
- Fast pickle loading vs text parsing
- Efficient large-scale experiments

## Relationship to Main Codebase

```
experiments/ (data generation)
    ↓ produces
pickled datasets (grids, pairs)
    ↓ consumed by
research scripts
    ↓ uses
f_search/ (algorithms, problems, solutions)
    ↓ produces
experimental results
```

## Key Properties

1. **One-time generation**: Create datasets once
2. **Reproducibility**: Same data across experiments
3. **Scalability**: Large datasets (1M pairs)
4. **Efficiency**: Fast pickle loading
5. **Research-oriented**: Designed for benchmarking
