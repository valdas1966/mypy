from f_log.utils import set_debug, log_1, log_2
from f_ds.grids import GridMap as Grid, CellMap as Cell
from f_utils import u_pickle, u_iter
from f_ds.pair import Pair as PairItem

Pair = PairItem[Cell]


set_debug(True)


@log_2
def load_grids(pickle_grids: str) -> dict[str, list[Grid]]:
    """
    ============================================================================
     Load the grids from the pickle file.
    ============================================================================
    """
    return u_pickle.load(path=pickle_grids)


@log_1
def generate_pairs_for_grid(grid: Grid, i: int) -> list[Pair]:
    """
    ============================================================================
     Generate pairs for a grid.
    ============================================================================
    """
    predicate = lambda x, y: x.distance(other=y) >= min_distance
    pairs: list[Pair] = u_iter.pairs(data=grid, size=size, predicate=predicate)
    return pairs


@log_2
def generate_pairs_for_grids(i: int,
                             grids: list[Grid]) -> dict[str, list[Pair]]:
    """
    ============================================================================
     Generate pairs for a list of grids.
    ============================================================================
    """
    d: dict[str, list[Pair]] = {}
    for i, grid in enumerate(grids):
        pairs = generate_pairs_for_grid(grid=grid, i=i)
        d[grid.name] = pairs
    return d


@log_2
def generate_pairs_for_domain(i: int,
                              domain: str,
                              grids: list[Grid]) -> dict[str, list[Pair]]:
    d: dict[str, list[Pair]] = generate_pairs_for_grids(i=i, grids=grids)


@log_2
def generate_pairs_for_domains(grids: dict[str, list[Grid]]) -> dict[str, dict[str, list[Pair]]]:
    grids: dict[str, list[Grid]] = load_grids()
    for i, domain in enumerate(grids.keys()):
        grid_pairs = generate_pairs_for_domain(i=i, domain=domain, grids=grids[domain])
        


size = 1_000_000
min_distance = 100