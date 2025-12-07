from f_ds.grids import CellMap as Cell
from f_math.percentiles.utils import UPercentiles
from f_math.percentiles.bin import Bin
from f_utils import u_pickle
from collections import defaultdict
import random
import time


def print_header() -> None:
    """
    ============================================================================
     Print the header of the potential pairs generation experiment.
    ============================================================================
    """
    print("=" * 80)
    print("Potential Cell Pairs Generation (Percentile-Based)")
    print("=" * 80)
    print()


def load_pairs_million() -> dict[str, dict[str, list[tuple[Cell, Cell, int]]]]:
    """
    ============================================================================
     Load the million pairs from the pickle file.
    ============================================================================
    """
    print("Loading pairs from g:\\paper\\pairs_million.pkl...")
    pairs = u_pickle.load(path='g:\\paper\\pairs_million.pkl')

    # Count total pairs
    total_pairs = sum(
        len(pairs_map)
        for domain_pairs in pairs.values()
        for pairs_map in domain_pairs.values()
    )

    print(f"Loaded {len(pairs)} domains")
    print(f"Total pairs: {total_pairs:,}")
    print()
    return pairs


def create_percentile_bins(distances: list[int]) -> list[Bin]:
    """
    ============================================================================
     Create percentile bins with step of 20% (20, 40, 60, 80, 100).
    ============================================================================
    """
    bins = UPercentiles.get_bins(values=distances, n_bins=20)
    return bins


def group_pairs_by_percentile(
    pairs: list[tuple[Cell, Cell, int]],
    bins: list[Bin]
) -> dict[int, list[tuple[Cell, Cell]]]:
    """
    ============================================================================
     Group pairs by their distance percentile.
     Returns dict[percentile, list[pairs_without_distance]].
    ============================================================================
    """
    # Initialize dict for each percentile
    percentile_groups: dict[int, list[tuple[Cell, Cell]]] = {
        bin.percentile: [] for bin in bins
    }

    # Group pairs by percentile
    for cell_a, cell_b, distance in pairs:
        # Find which bin this distance falls into
        for bin in bins:
            if distance in bin:  # Uses Bin.__contains__
                percentile_groups[bin.percentile].append((cell_a, cell_b))
                break

    return percentile_groups


def sample_pairs_from_groups(
    percentile_groups: dict[int, list[tuple[Cell, Cell]]],
    sample_size: int = 100
) -> dict[int, list[tuple[Cell, Cell]]]:
    """
    ============================================================================
     Sample up to sample_size pairs from each percentile group.
     If fewer pairs available, take all.
    ============================================================================
    """
    sampled_groups: dict[int, list[tuple[Cell, Cell]]] = {}

    for percentile, pairs in percentile_groups.items():
        if len(pairs) <= sample_size:
            # Take all pairs if fewer than sample_size
            sampled_groups[percentile] = pairs
        else:
            # Randomly sample sample_size pairs
            sampled_groups[percentile] = random.sample(pairs, sample_size)

    return sampled_groups


def process_all_pairs(
    pairs_million: dict[str, dict[str, list[tuple[Cell, Cell, int]]]]
) -> dict[str, dict[str, dict[int, list[tuple[Cell, Cell]]]]]:
    """
    ============================================================================
     Process all pairs and create percentile-based groupings.
     Returns dict[domain, dict[map_name, dict[percentile, pairs]]].
    ============================================================================
    """
    result: dict[str, dict[str, dict[int, list[tuple[Cell, Cell]]]]] = defaultdict(dict)

    # Count total maps
    total_maps = sum(len(maps) for maps in pairs_million.values())
    map_count = 0

    print("Processing pairs by percentile...")
    print("-" * 80)
    print()

    # Process each domain
    for domain, maps in pairs_million.items():
        print(f"Domain: {domain}")
        print("  " + "-" * 76)

        # Process each map
        for map_name, pairs in maps.items():
            map_count += 1
            print(f"  [{map_count}/{total_maps}] Map: {map_name}")
            print(f"    Total pairs: {len(pairs):,}")

            # Extract distances
            distances = [distance for _, _, distance in pairs]

            # Create percentile bins
            bins = create_percentile_bins(distances)
            print(f"    Percentile bins created: {len(bins)}")

            # Group pairs by percentile
            percentile_groups = group_pairs_by_percentile(pairs, bins)

            # Sample up to 100 pairs from each percentile
            sampled_groups = sample_pairs_from_groups(percentile_groups, sample_size=100)

            # Store results
            result[domain][map_name] = sampled_groups

            # Print statistics per percentile
            for percentile in sorted(sampled_groups.keys()):
                num_pairs = len(sampled_groups[percentile])
                print(f"      Percentile {percentile:3d}: {num_pairs:3d} pairs sampled")

            print()

        print()

    return result


def save_results(
    pairs_potential: dict[str, dict[str, dict[int, list[tuple[Cell, Cell]]]]],
    output_path: str
) -> None:
    """
    ============================================================================
     Save the percentile-based pairs to pickle file.
    ============================================================================
    """
    print("=" * 80)
    print(f"Saving results to {output_path}...")
    u_pickle.dump(obj=pairs_potential, path=output_path)
    print("Results saved successfully!")
    print()


def print_summary(
    pairs_potential: dict[str, dict[str, dict[int, list[tuple[Cell, Cell]]]]],
    elapsed: float
) -> None:
    """
    ============================================================================
     Print summary statistics.
    ============================================================================
    """
    # Calculate statistics
    total_domains = len(pairs_potential)
    total_maps = sum(len(maps) for maps in pairs_potential.values())

    total_pairs = sum(
        len(pairs)
        for domain_maps in pairs_potential.values()
        for map_pairs in domain_maps.values()
        for pairs in map_pairs.values()
    )

    # Percentiles used
    percentiles_used = set()
    for domain_maps in pairs_potential.values():
        for map_pairs in domain_maps.values():
            percentiles_used.update(map_pairs.keys())

    print("=" * 80)
    print("Summary")
    print("=" * 80)
    print(f"Total domains: {total_domains}")
    print(f"Total maps: {total_maps}")
    print(f"Percentiles: {sorted(percentiles_used)}")
    print(f"Total pairs sampled: {total_pairs:,}")
    print(f"Time elapsed: {elapsed:.2f} seconds ({elapsed/60:.2f} minutes)")
    print(f"Average time per map: {elapsed/total_maps:.2f} seconds")
    print()


# Main execution
if __name__ == "__main__":
    # Start timer
    start_time = time.time()

    # Print header
    print_header()

    # Load million pairs
    pairs_million = load_pairs_million()

    # Process pairs and create percentile old_groups
    pairs_potential = process_all_pairs(pairs_million)

    # Save results
    output_path = 'g:\\paper\\pairs_potential.pkl'
    save_results(pairs_potential, output_path)

    # Print summary
    elapsed = time.time() - start_time
    print_summary(pairs_potential, elapsed)

    print("=" * 80)
    print("Potential pairs generation completed!")
    print("=" * 80)
