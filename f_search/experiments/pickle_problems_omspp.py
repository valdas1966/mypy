from f_ds.grids import GridMap as Grid, CellMap as Cell
from f_utils import u_pickle
from collections import defaultdict
import random
import time


def print_header() -> None:
    """
    ============================================================================
     Print the header of the script.
    ============================================================================
    """
    print("=" * 80)
    print("Generate OMSPP Problems from Grids and Pairs")
    print("=" * 80)
    print()


def load_grids() -> dict[str, dict[str, Grid]]:
    """
    ============================================================================
     Load the grids from the pickle file.
     Structure: domain->map->Grid
    ============================================================================
    """
    print("Loading grids from g:\\paper\\grids.pkl...")
    grids = u_pickle.load(path='g:\\paper\\grids.pkl')

    total_grids = sum(len(maps) for maps in grids.values())
    print(f"Loaded {len(grids)} domains")
    print(f"Total grids: {total_grids}")
    print()
    return grids


def load_pairs() -> dict[str, dict[str, dict[int, list[tuple[Cell, Cell]]]]]:
    """
    ============================================================================
     Load the pairs from the pickle file.
     Structure: domain->map->percentile->list[5 pairs]
    ============================================================================
    """
    print("Loading pairs from g:\\paper\\pairs_5.pkl...")
    pairs = u_pickle.load(path='g:\\paper\\pairs_5.pkl')

    total_pairs = sum(
        len(pairs_list)
        for domain_maps in pairs.values()
        for map_pairs in domain_maps.values()
        for pairs_list in map_pairs.values()
    )

    print(f"Loaded {len(pairs)} domains")
    print(f"Total pairs: {total_pairs}")
    print()
    return pairs


def get_random_goals_around(
    grid: Grid,
    center_goal: Cell,
    start: Cell,
    num_goals: int,
    max_attempts: int = 100
) -> list[Cell] | None:
    """
    ============================================================================
     Get random goals around the center goal within a 10x10 box.
     Returns None if cannot find enough valid goals after max_attempts.
    ============================================================================
    """
    center_row = center_goal.row
    center_col = center_goal.col

    # Define 10x10 box bounds (center ±5)
    min_row = max(0, center_row - 5)
    max_row = min(grid.rows - 1, center_row + 5)
    min_col = max(0, center_col - 5)
    max_col = min(grid.cols - 1, center_col + 5)

    # Collect all valid cells in the box
    valid_cells = []
    for row in range(min_row, max_row + 1):
        for col in range(min_col, max_col + 1):
            cell = grid[row][col]
            # Must be passable and not start or center_goal
            if cell and cell != start and cell != center_goal:
                valid_cells.append(cell)

    # Check if we have enough valid cells
    if len(valid_cells) < num_goals:
        return None

    # Try to randomly select goals
    for attempt in range(max_attempts):
        selected = random.sample(valid_cells, num_goals)
        # Additional validation can be added here if needed
        return selected

    return None


def create_omspp_problems(
    grids: dict[str, dict[str, Grid]],
    pairs: dict[str, dict[str, dict[int, list[tuple[Cell, Cell]]]]]
) -> dict[str, dict[str, dict[int, list[dict]]]]:
    """
    ============================================================================
     Create OMSPP problems from grids and pairs.
     For each percentile with 5 pairs:
       - Pair 1 -> 10 goals
       - Pair 2 -> 20 goals
       - Pair 3 -> 30 goals
       - Pair 4 -> 40 goals
       - Pair 5 -> 50 goals

     Returns: domain->map->percentile->list[problem_dicts]
    ============================================================================
    """
    problems: dict[str, dict[str, dict[int, list[dict]]]] = defaultdict(lambda: defaultdict(dict))

    total_percentiles = sum(
        len(map_pairs)
        for domain_maps in pairs.values()
        for map_pairs in domain_maps.values()
    )

    percentile_count = 0
    total_problems_created = 0
    total_problems_skipped = 0

    print("Creating OMSPP problems...")
    print("-" * 80)
    print()

    # Goal counts for each pair index
    goal_counts = [10, 20, 30, 40, 50]

    # Process each domain
    for domain, maps in pairs.items():
        print(f"Domain: {domain}")
        print("  " + "-" * 76)

        # Process each map
        for map_name, percentile_pairs in maps.items():
            # Get the grid for this map
            if domain not in grids or map_name not in grids[domain]:
                print(f"  Map: {map_name} - Grid not found, skipping all percentiles")
                continue

            grid = grids[domain][map_name]

            # Process each percentile
            for percentile, pairs_list in percentile_pairs.items():
                percentile_count += 1
                print(f"  [{percentile_count}/{total_percentiles}] Map: {map_name}, Percentile: {percentile}")

                if len(pairs_list) != 5:
                    print(f"    WARNING: Expected 5 pairs, got {len(pairs_list)}, skipping")
                    continue

                percentile_problems = []

                # Process each pair with corresponding goal count
                for pair_idx, (start_cell, first_goal_cell) in enumerate(pairs_list):
                    num_goals = goal_counts[pair_idx]
                    num_random_goals = num_goals - 1  # Subtract the first goal

                    # Get random goals around the first goal
                    random_goals = get_random_goals_around(
                        grid=grid,
                        center_goal=first_goal_cell,
                        start=start_cell,
                        num_goals=num_random_goals,
                        max_attempts=100
                    )

                    if random_goals is None:
                        print(f"    Pair {pair_idx + 1} ({num_goals} goals): SKIPPED (insufficient valid cells)")
                        total_problems_skipped += 1
                        continue

                    # Combine first goal with random goals
                    all_goals = [first_goal_cell] + random_goals

                    # Create problem dictionary (minimal data, no Grid object)
                    problem_dict = {
                        'domain': domain,
                        'map': map_name,
                        'start': start_cell,
                        'goals': all_goals,
                        'num_goals': num_goals
                    }

                    percentile_problems.append(problem_dict)
                    total_problems_created += 1
                    print(f"    Pair {pair_idx + 1} ({num_goals} goals): Created")

                # Store problems for this percentile
                if percentile_problems:
                    problems[domain][map_name][percentile] = percentile_problems

                print()

        print()

    print(f"Total problems created: {total_problems_created}")
    print(f"Total problems skipped: {total_problems_skipped}")
    print()

    return dict(problems)


def save_results(
    problems: dict[str, dict[str, dict[int, list[dict]]]],
    output_path: str
) -> None:
    """
    ============================================================================
     Save the OMSPP problems to pickle file.
    ============================================================================
    """
    print("=" * 80)
    print(f"Saving results to {output_path}...")
    u_pickle.dump(obj=problems, path=output_path)
    print("Results saved successfully!")
    print()


def print_summary(
    problems: dict[str, dict[str, dict[int, list[dict]]]],
    elapsed: float
) -> None:
    """
    ============================================================================
     Print summary statistics.
    ============================================================================
    """
    total_domains = len(problems)
    total_maps = sum(len(maps) for maps in problems.values())

    total_problems = sum(
        len(problem_list)
        for domain_maps in problems.values()
        for map_problems in domain_maps.values()
        for problem_list in map_problems.values()
    )

    # Count by goal size
    goal_counts = {10: 0, 20: 0, 30: 0, 40: 0, 50: 0}
    for domain_maps in problems.values():
        for map_problems in domain_maps.values():
            for problem_list in map_problems.values():
                for problem in problem_list:
                    num_goals = problem['num_goals']
                    if num_goals in goal_counts:
                        goal_counts[num_goals] += 1

    print("=" * 80)
    print("Summary")
    print("=" * 80)
    print(f"Total domains: {total_domains}")
    print(f"Total maps: {total_maps}")
    print(f"Total problems: {total_problems}")
    print()
    print("Problems by goal count:")
    for num_goals in sorted(goal_counts.keys()):
        print(f"  {num_goals} goals: {goal_counts[num_goals]} problems")
    print()
    print(f"Time elapsed: {elapsed:.2f} seconds ({elapsed/60:.2f} minutes)")
    if total_problems > 0:
        print(f"Average time per problem: {elapsed/total_problems:.3f} seconds")
    print()


# Main execution
if __name__ == "__main__":
    # Start timer
    start_time = time.time()

    # Print header
    print_header()

    # Load grids
    grids = load_grids()

    # Load pairs
    pairs = load_pairs()

    # Create OMSPP problems
    problems = create_omspp_problems(grids, pairs)

    # Save results
    output_path = 'g:\\paper\\problems_omspp.pkl'
    save_results(problems, output_path)

    # Print summary
    elapsed = time.time() - start_time
    print_summary(problems, elapsed)

    print("=" * 80)
    print("OMSPP problems generation completed!")
    print("=" * 80)
