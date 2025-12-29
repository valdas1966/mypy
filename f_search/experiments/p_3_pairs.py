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
def gen_pairs(grids: dict[str, Grid],
                             pickle_black_cells: str,
                             size: int,
                             min_distance: int) -> dict[str, list[Pair]]:
    """
    ============================================================================
     Generate Random-Pairs for a List of Grids.
    ============================================================================
    """
    @log_2
    def for_grid(grid: Grid, total: int, i: int) -> list[Pair]:
        """
        ========================================================================
         Generate Random-Pairs for a given Grid (above the given min_distance).
        ========================================================================
        """ 
        cells_valid = set(grid.cells_valid()) - black_cells[grid.name]
        p_1 = lambda a, b: a.distance(other=b) >= min_distance 
        p_2 = lambda a, b: are_reachable(grid, a, b)
        predicate = lambda a, b: p_1(a, b) and p_2(a, b)
        pairs: list[Pair] = u_iter.pairs(items=cells_valid,
                                         size=size,
                                         predicate=predicate)
        return pairs
    
    black_cells = u_pickle.load(pickle_black_cells)
    total = len(grids)
    d: dict[str, list[Pair]] = dict()
    for i, (name, grid) in enumerate(grids.items()):
        pairs = for_grid(grid=grid, total=total, i=i+1)
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
 Input: Pickle of dict[Grid.Name -> Grid].
 Output: Pickle of dict[Grid.Name -> List[Pair]].
===============================================================================
"""

set_debug(True)
pickle_grids = 'f:\\paper\\i_1_grids\\grids.pkl'
pickle_black_cells = 'f:\\paper\\i_2_black_cells\\black_cells.pkl'
pickle_pairs = 'f:\\paper\\i_3_pairs\\pairs.pkl'
# Number of Pairs to Generate for each Grid.
size = 5
# Minimum Distance between the Pairs.
min_distance = 100

@log_2
def main(pickle_grids: str,
         pickle_black_cells: str,
         pickle_pairs: str) -> None:
    """
    ========================================================================
     Main
    ========================================================================
    """    
    grids = load_grids(pickle_grids)
    pairs = gen_pairs(grids,
                      pickle_black_cells,
                      size,
                      min_distance)
    pairs_to_pickle(pairs, pickle_pairs)

main(pickle_grids, pickle_black_cells, pickle_pairs)
