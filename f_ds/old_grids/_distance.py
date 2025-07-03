from collections.abc import Iterable
from f_ds.grids.cell.map.main import CellMap


class Distance:
    """
    ============================================================================
     Distance-Class for calculating distances between Cells.
    ============================================================================
    """

    @staticmethod
    def between(cell_a: CellMap, cell_b: CellMap) -> int:
        """
        ========================================================================
         Return the Manhattan-Distance between the two given Cells.
        ========================================================================
        """
        diff_row = abs(cell_a.row - cell_b.row)
        diff_col = abs(cell_a.col - cell_b.col)
        return diff_row + diff_col

    @staticmethod
    def avg(cells: Iterable[CellMap]) -> int:
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
                sum_dist += Distance.between(cell, other)
        return round(sum_dist / len(cells))
    
    @staticmethod
    def farthest(cell: CellMap, others: Iterable[CellMap]) -> CellMap:
        """
        ========================================================================
         Return the farthest other Cell from the given Cell.
        ========================================================================
        """
        # Init max values with not-logical values
        # (so that the first candidate will be good)
        dist_max = 0
        cell_max = None
        # Iterate over the candidates to find the farthest one
        for other in others:
            # Get the distance between the current cell and the candidate
            dist = Distance.between(cell, other)
            # Update the max distance and candidate if the current distance
            #  is greater than the current max distance.
            if dist > dist_max:
                dist_max = dist
                cell_max = cell
        # Return the farthest cell
        return cell_max
            
    