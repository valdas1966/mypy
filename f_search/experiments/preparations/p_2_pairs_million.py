from f_log.utils import set_debug, log_1, log_2
from f_ds.grids import GridMap as Grid, CellMap as Cell
from f_utils import u_pickle
from collections import defaultdict


@log_1
def load_grids(pickle_grids: str) -> dict[str, list[Grid]]:
    """
    ============================================================================
     Load the grids from the pickle file.
    ============================================================================
    """
    return u_pickle.load(path=pickle_grids)

