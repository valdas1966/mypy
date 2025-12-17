from f_log.utils import set_debug, log_1, log_2
from f_ds.grids import GridMap as Grid, CellMap as Cell
from f_utils import u_pickle, u_iter
from typing import Tuple

Pair = Tuple[Cell, Cell]


@log_2
def load_grids(pickle_grids: str) -> dict[str, Grid]:
    """
    ============================================================================
     Load the grids from the pickle file.
    ============================================================================
    """
    return u_pickle.load(path=pickle_grids)


@log_2
def generate_pairs_for_grids(i: int,
                             grids: list[Grid]) -> dict[str, list[Pair]]:
    """
    ============================================================================
     Generate Random-Pairs for a List of Grids.
    ============================================================================
    """
    @log_1
    def generate_pairs_for_grid(grid: Grid, i: int) -> list[Pair]:
        """
        ========================================================================
         Generate Random-Pairs for a given Grid (above the given min_distance).
        ========================================================================
        """
        predicate = lambda x, y: x.distance(other=y) >= min_distance
        pairs: list[Pair] = u_iter.pairs(data=grid,
                                        size=size,
                                        predicate=predicate)
        return pairs
    
    d: dict[str, list[Pair]] = dict()
    for i, grid in enumerate(grids):
        pairs = generate_pairs_for_grid(grid=grid, i=i)
        d[grid.name] = pairs
    return d
        
"""
===============================================================================
 Main - Generate Random-Pairs for a List of Grids.
-------------------------------------------------------------------------------
 Input: Pickle of dict[Grid.Name, Grid].
 Output: Pickle of dict[Grid.Name, List[Pair]].
===============================================================================
"""

set_debug(True)
pickle_grids = 'f:\\paper\\i_1_grids\\grids.pkl'
pickle_pairs = 'f:\\paper\\i_2_pairs\\pairs.pkl'
size = 1_000_000
min_distance = 100

@log_2
def main(pickle_grids: str, pickle_pairs: str) -> None:
    """
    ========================================================================
     Main
    ========================================================================
    """    
    grids = load_grids(pickle_grids=pickle_grids)
    pairs = generate_pairs_for_grids(grids=grids)
    u_pickle.dump(obj=pairs, path=pickle_pairs)

main(pickle_grids=pickle_grids,
     pickle_pairs=pickle_pairs)
