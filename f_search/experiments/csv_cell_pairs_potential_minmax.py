import csv
from f_ds.grids import CellMap as Cell
from f_utils import u_pickle


def load_pairs_potential(pickle_path: str) -> dict[str, dict[str, dict[int, list[tuple[Cell, Cell]]]]]:
    """
    ============================================================================
     Load the pairs_potential from the pickle file.
    ============================================================================
    """
    print(f"Loading pairs from {pickle_path}...")
    pairs = u_pickle.load(path=pickle_path)
    print(f"Loaded {len(pairs)} domains")
    print()
    return pairs


def calculate_manhattan_distance(cell_1: Cell, cell_2: Cell) -> int:
    """
    ============================================================================
     Calculate Manhattan distance between two cells.
    ============================================================================
    """
    return abs(cell_1.row - cell_2.row) + abs(cell_1.col - cell_2.col)


def convert_to_csv_minmax(
    pairs_potential: dict[str, dict[str, dict[int, list[tuple[Cell, Cell]]]]],
    output_path: str
) -> None:
    """
    ============================================================================
     Convert the pickle data to CSV format with min/max/avg statistics.
     CSV columns: graph, percentile, min_distance, max_distance, avg_distance
    ============================================================================
    """
    print(f"Converting to CSV: {output_path}")
    print("-" * 80)

    total_rows = 0

    with open(output_path, 'w', newline='') as csvfile:
        writer = csv.writer(csvfile)

        # Write header
        writer.writerow([
            'graph',
            'percentile',
            'min_distance',
            'max_distance',
            'avg_distance'
        ])

        # Process each domain
        for domain, maps in pairs_potential.items():
            print(f"Domain: {domain}")

            # Process each map
            for map_name, percentile_groups in maps.items():
                # Create full graph name (domain + map_name)
                graph_name = f"{domain}/{map_name}"

                # Process each percentile
                for percentile, pairs in percentile_groups.items():
                    if not pairs:
                        continue

                    # Calculate distances for all pairs
                    distances = [
                        calculate_manhattan_distance(cell_1, cell_2)
                        for cell_1, cell_2 in pairs
                    ]

                    # Calculate statistics
                    min_distance = min(distances)
                    max_distance = max(distances)
                    avg_distance = sum(distances) / len(distances)

                    # Write row
                    writer.writerow([
                        graph_name,
                        percentile,
                        min_distance,
                        max_distance,
                        f"{avg_distance:.2f}"
                    ])

                    total_rows += 1

                print(f"  {map_name}: {len(percentile_groups)} percentile groups")

            print()

    print(f"Total rows written: {total_rows:,}")
    print(f"CSV saved to: {output_path}")
    print()


def print_summary(csv_path: str) -> None:
    """
    ============================================================================
     Print summary of the CSV file.
    ============================================================================
    """
    print("=" * 80)
    print("Summary")
    print("=" * 80)

    # Count rows
    with open(csv_path, 'r') as csvfile:
        reader = csv.reader(csvfile)
        next(reader)  # Skip header
        row_count = sum(1 for _ in reader)

    print(f"Total data rows: {row_count:,}")
    print(f"CSV file: {csv_path}")
    print()


# Main execution
if __name__ == "__main__":
    print("=" * 80)
    print("Convert Pairs Potential Pickle to CSV (Min/Max/Avg)")
    print("=" * 80)
    print()

    # Input and output paths
    pickle_path = 'g:\\paper\\pairs_potential.pkl'
    csv_path = 'g:\\paper\\pairs_potential_minmax.csv'

    # Load pickle data
    pairs_potential = load_pairs_potential(pickle_path)

    # Convert to CSV with min/max/avg statistics
    convert_to_csv_minmax(pairs_potential, csv_path)

    # Print summary
    print_summary(csv_path)

    print("=" * 80)
    print("Conversion completed!")
    print("=" * 80)
