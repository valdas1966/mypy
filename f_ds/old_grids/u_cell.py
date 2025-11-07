from typing import Iterable
from f_ds.old_grids.old_cell import Cell


class UCell:
    """
    ============================================================================
     Utils for Cell class.
    ============================================================================
    """

    @staticmethod
    def farthest(base: Cell, cands: Iterable[Cell]) -> Cell:
        """
        ========================================================================
         Return the farthest candidate Cell from the Base Cell.
        ========================================================================
        """
        # Set the initial max distance to zero
        #  (because must be greater than 0)
        dist_max = 0
        # Set the initial candidate to None
        cand_max = None
        # Iterate over the candidates to find the farthest one
        for cand in cands:
            # Get the distance between the i_0_base and the candidate
            dist = base.distance(cand)
            # Update the max distance and candidate if the current distance
            #  is greater than the current max distance.
            if dist > dist_max:
                dist_max = dist
                cand_max = cand
        return cand_max
