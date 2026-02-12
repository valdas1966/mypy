from __future__ import annotations

import csv
from pathlib import Path
from typing import Any

from f_utils import u_pickle


def diamonds_pickle_to_csv(pickle_path: str, csv_path: str) -> None:
    """
    Pickle format expected:
      dict[str, list[tuple[Diamond, Diamond]]]
    where Diamond is typically list[State] (or any iterable of states).

    Output CSV columns:
      grid_name, len_diamond_a, len_diamond_b
    """
    pickle_path = str(Path(pickle_path))
    csv_path = str(Path(csv_path))

    diamonds: dict[str, list[Any]] = u_pickle.load(path=pickle_path)

    with open(csv_path, "w", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        w.writerow(["grid_name", "len_diamond_a", "len_diamond_b"])

        for grid_name, pairs in diamonds.items():
            for pair in pairs:
                diamond_a, diamond_b = pair
                w.writerow([grid_name, len(diamond_a), len(diamond_b)])


if __name__ == "__main__":
    pickle_diamonds = r"f:\paper\i_2_diamonds\diamonds.pkl"
    csv_out = r"f:\paper\i_2_diamonds\diamonds.csv"
    diamonds_pickle_to_csv(pickle_diamonds, csv_out)
    print("Wrote:", csv_out)
