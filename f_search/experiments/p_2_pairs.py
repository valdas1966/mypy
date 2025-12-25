from f_log.utils import set_debug, log_2
from f_ds.grids import GridMap as Grid, CellMap as Cell
from f_search.algos.i_1_spp.utils import are_reachable
from f_utils import u_pickle, u_iter

Pair = tuple[Cell, Cell]


@log_2
def load_grids(pickle_grids: str) -> dict[str, Grid]:
    """
    ============================================================================
     Load the grids from the pickle file.
    ============================================================================
    """
    return u_pickle.load(path=pickle_grids)


@log_2
def generate_pairs_for_grids(grids: dict[str, Grid],
                             size: int,
                             min_distance: int) -> dict[str, list[Pair]]:
    """
    ============================================================================
     Generate Random-Pairs for a List of Grids.
    ============================================================================
    """
    @log_2
    def for_grid(grid: Grid, i: int) -> list[Pair]:
        """
        ========================================================================
         Generate Random-Pairs for a given Grid (above the given min_distance).
        ========================================================================
        """ 
        p_1 = lambda x, y: x.distance(other=y) >= min_distance
        p_2 = lambda x, y: are_reachable(grid, x, y)
        predicate = lambda x, y: p_1(x, y) and p_2(x, y)
        pairs: list[Pair] = u_iter.pairs(items=grid,
                                         size=size,
                                         predicate=predicate)
        return pairs
    
    d: dict[str, list[Pair]] = dict()
    for i, (name, grid) in enumerate(grids.items()):
        pairs = for_grid(grid=grid, i=i)
        d[name] = pairs
    return d


@log_2
def pairs_to_pickle(pairs: dict[str, list[Pair]], pickle_pairs: str) -> None:
    """
    ========================================================================
     Pickle the List[Pair] to the given path.
    ========================================================================
    """
    u_pickle.dump(obj=pairs, path=pickle_pairs)

        
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
size = 5
min_distance = 100

@log_2
def main(pickle_grids: str, pickle_pairs: str) -> None:
    """
    ========================================================================
     Main
    ========================================================================
    """    
    grids = load_grids(pickle_grids)
    pairs = generate_pairs_for_grids(grids, size, min_distance)
    pairs_to_pickle(pairs, pickle_pairs)

main(pickle_grids, pickle_pairs)
