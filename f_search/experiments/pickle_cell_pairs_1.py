from f_ds.grids import CellMap as Cell
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
    print("Extract One Random Pair per Domain->Map->Percentile")
    print("=" * 80)
    print()


def load_pairs_potential() -> dict[str, dict[str, dict[int, list[tuple[Cell, Cell]]]]]:
    """
    ============================================================================
     Load the pairs_potential from the pickle file.
    ============================================================================
    """
    print("Loading pairs from g:\\paper\\pairs_potential.pkl...")
    pairs = u_pickle.load(path='g:\\paper\\pairs_potential.pkl')

    # Count total pairs
    total_pairs = sum(
        len(pairs_list)
        for domain_maps in pairs.values()
        for map_pairs in domain_maps.values()
        for pairs_list in map_pairs.values()
    )

    print(f"Loaded {len(pairs)} domains")
    print(f"Total pairs: {total_pairs:,}")
    print()
    return pairs


def extract_one_pair_per_group(
    pairs_potential: dict[str, dict[str, dict[int, list[tuple[Cell, Cell]]]]]
) -> tuple[
    dict[str, dict[str, dict[int, tuple[Cell, Cell]]]],
    dict[str, dict[str, dict[int, list[tuple[Cell, Cell]]]]]
]:
    """
    ============================================================================
     Extract one random pair from each domain->map->percentile combination.
     Returns:
         - pairs_1: dict with single pair per domain->map->percentile
         - pairs_remaining: dict with remaining pairs (original with selected pairs removed)
    ============================================================================
    """
    pairs_1: dict[str, dict[str, dict[int, tuple[Cell, Cell]]]] = defaultdict(lambda: defaultdict(dict))
    pairs_remaining: dict[str, dict[str, dict[int, list[tuple[Cell, Cell]]]]] = defaultdict(lambda: defaultdict(dict))

    total_groups = sum(
        len(map_pairs)
        for domain_maps in pairs_potential.values()
        for map_pairs in domain_maps.values()
    )

    group_count = 0

    print("Extracting one random pair per domain->map->percentile...")
    print("-" * 80)
    print()

    # Process each domain
    for domain, maps in pairs_potential.items():
        print(f"Domain: {domain}")
        print("  " + "-" * 76)

        # Process each map
        for map_name, percentile_pairs in maps.items():
            group_count += 1
            print(f"  [{group_count}/{total_groups}] Map: {map_name}")

            # Process each percentile
            for percentile, pairs_list in percentile_pairs.items():
                if len(pairs_list) == 0:
                    print(f"    Percentile {percentile:3d}: No pairs available (skipping)")
                    continue

                # Select one random pair
                selected_pair = random.choice(pairs_list)
                pairs_1[domain][map_name][percentile] = selected_pair

                # Store remaining pairs (all except the selected one)
                remaining = [p for p in pairs_list if p != selected_pair]
                pairs_remaining[domain][map_name][percentile] = remaining

                print(f"    Percentile {percentile:3d}: Selected 1 pair, {len(remaining)} remaining")

            print()

        print()

    return dict(pairs_1), dict(pairs_remaining)


def save_results(
    pairs_1: dict[str, dict[str, dict[int, tuple[Cell, Cell]]]],
    pairs_remaining: dict[str, dict[str, dict[int, list[tuple[Cell, Cell]]]]],
) -> None:
    """
    ============================================================================
     Save the results:
     - pairs_1.pkl: single pairs
     - pairs_potential.pkl: updated with remaining pairs
    ============================================================================
    """
    print("=" * 80)
    print("Saving results...")

    # Save single pairs
    pairs_1_path = 'g:\\paper\\pairs_1.pkl'
    print(f"  Saving pairs_1 to {pairs_1_path}...")
    u_pickle.dump(obj=pairs_1, path=pairs_1_path)

    # Save remaining pairs (overwrite original)
    pairs_potential_path = 'g:\\paper\\pairs_potential.pkl'
    print(f"  Updating {pairs_potential_path}...")
    u_pickle.dump(obj=pairs_remaining, path=pairs_potential_path)

    print("Results saved successfully!")
    print()


def print_summary(
    pairs_1: dict[str, dict[str, dict[int, tuple[Cell, Cell]]]],
    pairs_remaining: dict[str, dict[str, dict[int, list[tuple[Cell, Cell]]]]],
    elapsed: float
) -> None:
    """
    ============================================================================
     Print summary statistics.
    ============================================================================
    """
    # Calculate statistics for pairs_1
    total_domains_1 = len(pairs_1)
    total_maps_1 = sum(len(maps) for maps in pairs_1.values())
    total_pairs_1 = sum(
        1
        for domain_maps in pairs_1.values()
        for map_pairs in domain_maps.values()
        for _ in map_pairs.values()
    )

    # Calculate statistics for remaining pairs
    total_pairs_remaining = sum(
        len(pairs_list)
        for domain_maps in pairs_remaining.values()
        for map_pairs in domain_maps.values()
        for pairs_list in map_pairs.values()
    )

    print("=" * 80)
    print("Summary")
    print("=" * 80)
    print(f"Pairs extracted to pairs_1.pkl:")
    print(f"  Domains: {total_domains_1}")
    print(f"  Maps: {total_maps_1}")
    print(f"  Total pairs: {total_pairs_1:,}")
    print()
    print(f"Pairs remaining in pairs_potential.pkl:")
    print(f"  Total pairs: {total_pairs_remaining:,}")
    print()
    print(f"Time elapsed: {elapsed:.2f} seconds")
    print()


# Main execution
if __name__ == "__main__":
    # Start timer
    start_time = time.time()

    # Print header
    print_header()

    # Load pairs_potential
    pairs_potential = load_pairs_potential()

    # Extract one pair per group and get remaining pairs
    pairs_1, pairs_remaining = extract_one_pair_per_group(pairs_potential)

    # Save results
    save_results(pairs_1, pairs_remaining)

    # Print summary
    elapsed = time.time() - start_time
    print_summary(pairs_1, pairs_remaining, elapsed)

    print("=" * 80)
    print("Extraction completed!")
    print("=" * 80)
