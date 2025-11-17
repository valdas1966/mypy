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


def convert_to_csv(
    pairs_potential: dict[str, dict[str, dict[int, list[tuple[Cell, Cell]]]]],
    output_path: str
) -> None:
    """
    ============================================================================
     Convert the pickle data to CSV format.
     CSV columns: graph_name, percentile, (Cell_1.row|Cell_1.col),
                  (Cell_2.row|Cell_2.col), distance
    ============================================================================
    """
    print(f"Converting to CSV: {output_path}")
    print("-" * 80)

    total_rows = 0

    with open(output_path, 'w', newline='') as csvfile:
        writer = csv.writer(csvfile)

        # Write header
        writer.writerow([
            'graph_name',
            'percentile',
            '(Cell_1.row|Cell_1.col)',
            '(Cell_2.row|Cell_2.col)',
            'distance'
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
                    # Process each pair
                    for cell_1, cell_2 in pairs:
                        # Calculate distance
                        distance = calculate_manhattan_distance(cell_1, cell_2)

                        # Format cell coordinates
                        cell_1_str = f"({cell_1.row}|{cell_1.col})"
                        cell_2_str = f"({cell_2.row}|{cell_2.col})"

                        # Write row
                        writer.writerow([
                            graph_name,
                            percentile,
                            cell_1_str,
                            cell_2_str,
                            distance
                        ])

                        total_rows += 1

                print(f"  {map_name}: {sum(len(pairs) for pairs in percentile_groups.values())} pairs")

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
    print("Convert Pairs Potential Pickle to CSV")
    print("=" * 80)
    print()

    # Input and output paths
    pickle_path = 'g:\\paper\\pairs_potential.pkl'
    csv_path = 'g:\\paper\\pairs_potential.csv'

    # Load pickle data
    pairs_potential = load_pairs_potential(pickle_path)

    # Convert to CSV
    convert_to_csv(pairs_potential, csv_path)

    # Print summary
    print_summary(csv_path)

    print("=" * 80)
    print("Conversion completed!")
    print("=" * 80)
