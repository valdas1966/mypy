from __future__ import annotations
from f_core.mixins.has_name import HasName
from f_core.mixins.has_rows_cols import HasRowsCols
from f_ds.mixins.groupable import Groupable, Group
from f_ds.groups.view import View
from f_ds.grids.cell import Cell
from f_file.map_grid import MapGrid
from collections.abc import Iterable
from typing import Iterator
import numpy as np
import random
import os


class Grid(HasName, HasRowsCols, Groupable[Cell], Iterable):
    """
    ============================================================================
     2D-Grid Class of Cells.
    ============================================================================
    """

    def __init__(self,
                 rows: int,
                 cols: int = None,
                 name: str = None) -> None:
        """
        ========================================================================
         Init private Attributes.
        ========================================================================
        """
        HasName.__init__(self, name=name)
        HasRowsCols.__init__(self, rows=rows, cols=cols)
        self._cells = [
                        [Cell(row, col) for col in range(self.cols)]
                        for row in range(self.rows)
                      ]
        self._cells_valid = View(name='Valid Cells',
                                 group=self.to_group(),
                                 predicate=bool)

    @property
    def cells_valid(self) -> View[Cell]:
        """
        ========================================================================
         Component-Class for Valid-Cells in the Grid.
        ========================================================================
        """
        return self._cells_valid

    def neighbors(self, cell: Cell) -> list[Cell]:
        """
        ========================================================================
         Return List of list valid Cell-Neighbors in Clockwise-Order.
        ========================================================================
        """
        cells_within = [self._cells[n.row][n.col]
                        for n
                        in cell.neighbors()
                        if self.is_within(n.row, n.col)]
        return [cell for cell in cells_within if cell]

    def distance_avg(self, cells: Iterable[Cell]) -> int:
        """
        ========================================================================
         Return the average distance between all the cells in the iterable.
        ========================================================================
        """
        sum_dist = 0
        for cell in cells:
            for other in cells:
                if cell >= other:
                    continue
                sum_dist += self.distance(cell, other)
        return round(sum_dist / len(cells))

    def random_cells_within_distance(self,
                                     cell: Cell,
                                     distance_max: int,
                                     distance_min: int = 1,
                                     epochs: int = 1,
                                     n: int = 1) -> set[Cell]:
        """
        ========================================================================
         Return a list of random valid cells within a given Distance-Range.
        ========================================================================
        """
        cells: set[Cell] = set()
        for _ in range(n*epochs):
            cell_random = self._random_cell_distance(cell=cell,
                                                     distance_min=distance_min,
                                                     distance_max=distance_max,
                                                     epochs=epochs)
            cells.add(cell_random)
            if len(cells) >= n:
                break
        return cells
    
    def random_cells_within_percentile(self,
                                       cell: Cell,
                                       percentile_max: int,
                                       percentile_min: int = 0,
                                       epochs: int = 1,
                                       n: int = 1) -> set[Cell]:
        """
        ========================================================================
         Return a list of random valid cells within a given Percentile-Range.
        ========================================================================
        """
        n_cells_valid = len(self.cells_valid)
        distance_min = max(1, round(n_cells_valid * percentile_min / 100))
        distance_max = round(n_cells_valid * percentile_max / 100)
        return self.random_cells_within_distance(cell=cell,
                                                 distance_min=distance_min,
                                                 distance_max=distance_max,
                                                 epochs=epochs,
                                                 n=n)
    
    def to_group(self, name: str = None) -> Group[Cell]:
        """
        ========================================================================
         Return list flattened list representation of the 2D Object.
        ========================================================================
        """
        return Group(name=name, data=list(self))
    
    def to_array(self) -> np.ndarray:
        """
        ========================================================================
         Return numpy boolean array representation of the Grid.
        ========================================================================
        """
        return np.array([[bool(cell) for cell in row]
                        for row in self._cells])
            
    @staticmethod
    def distance(cell_a: Cell, cell_b: Cell) -> int:
        """
        ========================================================================
         Return list Manhattan-Distance between the two given Cells.
        ========================================================================
        """
        diff_row = abs(cell_a.row - cell_b.row)
        diff_col = abs(cell_a.col - cell_b.col)
        return diff_row + diff_col

    def __getitem__(self, index) -> list[Cell]:
        """
        ========================================================================
         1. Direct access to list Row of Cells via the [Row] Property.
         2. Direct access specific Cell using [Row][Col] Properties.
        ========================================================================
        """
        return self._cells[index]

    def __str__(self) -> str:
        """
        ========================================================================
         Plot the Grid with (0,1) values.
        ========================================================================
        """
        # Cols Title
        res = '  ' + ' '.join((str(col) for col in range(self.cols))) + '\n'
        for row in range(self.rows):
            res += str(row) + ' '
            for col in range(self.cols):
                res += '1 ' if self._cells[row][col] else '0 '
            res += '\n'
        return res

    def __iter__(self) -> Iterator[Cell]:
        """
        ========================================================================
         Allow iteration over Cells in the Grid (flattened mode).
        ========================================================================
        """
        return (cell for row in self._cells for cell in row)

    @classmethod
    def generate(cls,
                 rows: int,
                 cols: int = None,
                 pct_valid: int = 100,
                 name: str = None) -> Grid:
        """
        ========================================================================
         Generate Grid with Random Valid-Cells based on list given Percentage.
        ========================================================================
        """
        grid = Grid(name=name, rows=rows, cols=cols)
        cells_to_invalidate = grid.sample(pct=100-pct_valid)
        Cell.invalidate(cells=cells_to_invalidate)
        return grid
    
    @classmethod
    def from_array(cls, array: np.ndarray, name: str = None) -> Grid:
        """
        ========================================================================
         Create a Grid from a numpy boolean array.
        ========================================================================
        """
        rows = array.shape[0]
        cols = array.shape[1]
        grid = Grid(name=name, rows=rows, cols=cols)
        for row in range(rows):
            for col in range(cols):
                if not array[row][col]:
                    grid[row][col].set_invalid()
        return grid

    @classmethod
    def from_map_grid(cls, path: str) -> Grid:
        """
        ========================================================================
         Create a Grid from a Map-Grid-File.
        ========================================================================
        """
        map_grid = MapGrid(path=path)
        name = os.path.splitext(os.path.basename(path))[0]
        array = map_grid.to_array()
        return cls.from_array(array=array, name=name)

    def _random_cell_distance(self,
                              cell: Cell,
                              distance_max: int,
                              distance_min: int = 1,
                              epochs: int = 1) -> Cell | None:
        """
        ========================================================================
         Return a random valid cell whose distance from the given cell is
           within [distance_min, distance_max].
        ========================================================================
        """
        row, col = cell.row, cell.col
        for _ in range(epochs):
            total_candidates = 0
            candidates_info = []
            
            # Determine feasible dc range, taking grid boundaries into account.
            dc_min = max(-distance_max, -col)
            dc_max = min(distance_max, self.cols - col - 1)
            
            for dc in range(dc_min, dc_max + 1):
                # For a given dc, allowed |dr| values are in [max(0, distance_min - |dc|), distance_max - |dc|]
                min_dr_abs = max(0, distance_min - abs(dc))
                max_dr_abs = distance_max - abs(dc)
                
                # Determine the range for dr given grid boundaries.
                dr_lower_bound = max(-max_dr_abs, -row)
                dr_upper_bound = min(max_dr_abs, self.rows - row - 1)
                
                valid_dr_values = []
                for dr in range(dr_lower_bound, dr_upper_bound + 1):
                    if abs(dr) >= min_dr_abs:
                        candidate_row = row + dr
                        candidate_col = col + dc
                        candidate_cell = self._cells[candidate_row][candidate_col]
                        # Only add candidate if the cell is valid (non-obstacle)
                        if candidate_cell:
                            valid_dr_values.append(dr)
                count = len(valid_dr_values)
                if count > 0:
                    candidates_info.append((dc, valid_dr_values, count))
                    total_candidates += count
            
            if total_candidates > 0:
                # Choose a random candidate uniformly among all possibilities.
                rand_index = random.randrange(total_candidates)
                for dc, valid_dr_values, count in candidates_info:
                    if rand_index < count:
                        chosen_dr = valid_dr_values[rand_index]
                        target_row = row + chosen_dr
                        target_col = col + dc
                        return self._cells[target_row][target_col]
                    else:
                        rand_index -= count
        return None
