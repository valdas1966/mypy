from f_ds.grids import GridMap as Grid, CellMap as Cell
from collections import defaultdict
from f_utils import u_pickle
import random
import time


def generate_pairs_for_grid(grid: Grid,
                            num_pairs: int = 1_000_000,
                            min_distance: int = 100) -> list[tuple[Cell, Cell, int]]:
    """
    ============================================================================
     Generate #num_pairs of cell-pairs where Manhattan distance >= min_distance.
    ============================================================================
    """
    # Get all reachable cells
    cells = grid.cells_valid()

    # List to store the pairs
    pairs: list[tuple[Cell, Cell, int]] = []
    # Counter to track the number of attempts of sampling per pair 
    # (to avoid infinite loops)
    attempts = 0
    # Safety limit to avoid infinite loops (10x the number of pairs)
    max_attempts = num_pairs * 10

    print(f"Generating {num_pairs:,} pairs from {len(cells):,} reachable cells...")

    # Generate pairs until the desired number is reached
    while len(pairs) < num_pairs:
        
        # Randomly sample two cells
        cell_a, cell_b = random.sample(population=cells, k=2)

        # Calculate Manhattan distance
        distance = cell_a.distance(other=cell_b)

        # Check if distance meets minimum requirement
        if distance >= min_distance:
            pairs.append((cell_a, cell_b, distance))
        
        # Progress update every 100k pairs
        if len(pairs) % 100_000 == 0:
            print(f"    Progress: {len(pairs):,}/{num_pairs:,} pairs generated")

        attempts += 1

        # Check if we're stuck (grid might be too small)
        if attempts >= max_attempts and len(pairs) < num_pairs:
            print(f"  WARNING: Only generated {len(pairs):,} valid pairs after {attempts:,} attempts")
            print(f"  Grid may be too small to generate {num_pairs:,} pairs with distance >= {min_distance}")
            break

    return pairs


def print_header() -> None:
    """
    ============================================================================
     Print the header of the cell pair generation experiment.
    ============================================================================
    """
    print("=" * 80)
    print("Cell Pair Generation Experiment")
    print("=" * 80)
    print()


def load_grids() -> dict[str, dict[str, Grid]]:
    """
    ============================================================================
     Load the grids from the pickle file.
    ============================================================================
    """
    # Load grids from pickle file
    print("Loading grids from /mnt/g/paper/grids.pkl...")
    grids = u_pickle.load(path='g:\\paper\\grids.pkl')
    print(f"Loaded {len(grids)} domains")
    print()
    return grids


def calc_total_grids(grids: dict[str, dict[str, Grid]]) -> int:
    """
    ============================================================================
     Calculate the total number of grids.
    ============================================================================
    """
    # Count total grids
    total_grids = sum(len(grids_domain) for grids_domain in grids.values())
    print(f"Total grids to process: {total_grids}")
    print()
    return total_grids


# Start time to output the total time elapsed
start_time = time.time()

# Print header of the script
print_header()

# Load grids
grids = load_grids()

# Calculate total number of grids
total_grids = calc_total_grids(grids)

# Generate pairs for each grid
dict_pairs = defaultdict(dict)
grid_count = 0

# Process each domain
for domain, grids_domain in grids.items():
    print(f"Processing domain: {domain}")
    print("-" * 80)

    for name_grid, grid in grids_domain.items():
        grid_count += 1
        print(f"\n[{grid_count}/{total_grids}] Grid: {name_grid}")
        print(f"  Dimensions: {grid.rows}x{grid.cols} ({len(grid):,} total cells)")

        # Generate pairs
        pairs = generate_pairs_for_grid(grid=grid)
        dict_pairs[domain][name_grid] = pairs

        print(f"  Generated {len(pairs):,} pairs")
    print()

# Save results
output_path = 'g:\\paper\\pairs.pkl'
print("=" * 80)
print(f"Saving results to {output_path}...")
u_pickle.dump(obj=dict_pairs, path=output_path)

# Summary
elapsed = time.time() - start_time
total_pairs = sum(len(pairs) for domain_pairs in dict_pairs.values() for pairs in domain_pairs.values())

print()
print("=" * 80)
print("Summary")
print("=" * 80)
print(f"Total grids processed: {total_grids}")
print(f"Total pairs generated: {total_pairs:,}")
print(f"Time elapsed: {elapsed:.2f} seconds ({elapsed/60:.2f} minutes)")
print(f"Average time per grid: {elapsed/total_grids:.2f} seconds")
print()
