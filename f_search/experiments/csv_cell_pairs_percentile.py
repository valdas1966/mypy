from f_ds.grids import CellMap as Cell
from f_math.percentiles.utils import UPercentiles
from f_math.percentiles.bin import Bin
from f_utils import u_pickle
import csv
import time


def print_header() -> None:
    """
    ============================================================================
     Print the header of the CSV generation experiment.
    ============================================================================
    """
    print("=" * 80)
    print("Generate CSV: Cell Pairs Count by Percentile")
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


def count_pairs_by_percentile(
    pairs: list[tuple[Cell, Cell, int]]
) -> dict[int, int]:
    """
    ============================================================================
     Count how many pairs fall into each percentile bin.
     Returns dict[percentile, count].
    ============================================================================
    """
    # Extract distances
    distances = [distance for _, _, distance in pairs]

    # Create percentile bins (20, 40, 60, 80, 100)
    bins = UPercentiles.get_bins(values=distances, n_bins=20)

    # Initialize counts for all percentiles (including missing ones)
    percentile_counts: dict[int, int] = {20: 0, 40: 0, 60: 0, 80: 0, 100: 0}

    # Count pairs in each bin
    for bin in bins:
        count = sum(1 for _, _, distance in pairs if distance in bin)
        percentile_counts[bin.percentile] = count

    return percentile_counts


def generate_csv_data(
    pairs_million: dict[str, dict[str, list[tuple[Cell, Cell, int]]]]
) -> list[dict[str, any]]:
    """
    ============================================================================
     Generate CSV data: list of rows with domain, graph, percentile, cnt.
    ============================================================================
    """
    csv_rows: list[dict[str, any]] = []

    # Count total maps
    total_maps = sum(len(maps) for maps in pairs_million.values())
    map_count = 0

    print("Generating CSV data...")
    print("-" * 80)
    print()

    # Process each domain
    for domain, maps in pairs_million.items():
        print(f"Domain: {domain}")

        # Process each map
        for map_name, pairs in maps.items():
            map_count += 1

            print(f"  [{map_count}/{total_maps}] {map_name} ({len(pairs):,} pairs)")

            # Count pairs by percentile
            percentile_counts = count_pairs_by_percentile(pairs)

            # Create rows for each percentile
            for percentile in [20, 40, 60, 80, 100]:
                csv_rows.append({
                    'domain': domain,
                    'graph': map_name,
                    'percentile': percentile,
                    'cnt': percentile_counts[percentile]
                })

        print()

    return csv_rows


def save_csv(csv_rows: list[dict[str, any]], output_path: str) -> None:
    """
    ============================================================================
     Save CSV data to file.
    ============================================================================
    """
    print("=" * 80)
    print(f"Saving CSV to {output_path}...")

    with open(output_path, 'w', newline='', encoding='utf-8') as csvfile:
        fieldnames = ['domain', 'graph', 'percentile', 'cnt']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

        # Write header
        writer.writeheader()

        # Write rows
        writer.writerows(csv_rows)

    print(f"CSV saved successfully! ({len(csv_rows)} rows)")
    print()


def print_summary(csv_rows: list[dict[str, any]], elapsed: float) -> None:
    """
    ============================================================================
     Print summary statistics.
    ============================================================================
    """
    # Calculate statistics
    unique_graphs = len(set(row['graph'] for row in csv_rows))
    total_pairs_counted = sum(row['cnt'] for row in csv_rows)

    # Count rows by percentile
    percentile_stats = {20: 0, 40: 0, 60: 0, 80: 0, 100: 0}
    for row in csv_rows:
        percentile_stats[row['percentile']] += row['cnt']

    print("=" * 80)
    print("Summary")
    print("=" * 80)
    print(f"Total graphs: {unique_graphs}")
    print(f"Total CSV rows: {len(csv_rows)}")
    print(f"Total pairs counted: {total_pairs_counted:,}")
    print()
    print("Pairs by percentile (across all graphs):")
    for percentile in [20, 40, 60, 80, 100]:
        print(f"  Percentile {percentile:3d}: {percentile_stats[percentile]:,}")
    print()
    print(f"Time elapsed: {elapsed:.2f} seconds ({elapsed/60:.2f} minutes)")
    print()


# Main execution
if __name__ == "__main__":
    # Start timer
    start_time = time.time()

    # Print header
    print_header()

    # Load million pairs
    pairs_million = load_pairs_million()

    # Generate CSV data
    csv_rows = generate_csv_data(pairs_million)

    # Save CSV
    output_path = 'g:\\paper\\pairs_percentile.csv'
    save_csv(csv_rows, output_path)

    # Print summary
    elapsed = time.time() - start_time
    print_summary(csv_rows, elapsed)

    print("=" * 80)
    print("CSV generation completed!")
    print("=" * 80)
