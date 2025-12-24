from f_log.utils import set_debug, log_2
from f_utils import u_pickle
from f_ds.grids import CellMap as Cell
from f_utils import u_iter

Pair = tuple[Cell, Cell]


@log_2
def load_pairs(pickle_pairs: str) -> dict[str, list[Pair]]:
    """
    ============================================================================
     Load the pairs from the pickle file.
    ============================================================================
    """
    return u_pickle.load(path=pickle_pairs)


@log_2
def assign_k_to_pairs(pairs: dict[str, list[Pair]],
                      k: list[int]) -> dict[str, dict[int, list[Pair]]]:
    """
    ============================================================================
     Assign the k to the pairs.
    ============================================================================
    """
    # Dictionary to store the assigned k to the pairs
    out: dict[str, dict[int, list[Pair]]] = dict()
    # Go over all grids
    for name, pairs in pairs.items():
        # Assign the k to the pairs for the current grid
        out[name] = u_iter.distribute(items=pairs, keys=k)
    # Return the dictionary
    return out

@log_2
def pickle_results(assigned_k: dict[str, dict[int, list[Pair]]],
                   pickle_k: str) -> None:
    """
    ============================================================================
     Pickle the results to the given path.
    ============================================================================
    """
    u_pickle.dump(obj=assigned_k, path=pickle_k)


"""
===============================================================================
 Main - Assign K to Pairs (by chunk slices).
-------------------------------------------------------------------------------
 Input: Pickle of [Grid.Name] -> List[Pair].
 Output: Pickle of [Grid.Name][K] -> List[Pair].
===============================================================================
"""

set_debug(True)
pickle_pairs = 'f:\\paper\\i_2_pairs\\pairs.pkl'
pickle_k = 'f:\\paper\\i_3_k\\k.pkl'
k = [10, 20, 30, 40, 50]

@log_2
def main(pickle_pairs: str, pickle_k: str, k: list[int]) -> None:
    """
    ========================================================================
     Main
    ========================================================================
    """    
    pairs = load_pairs(pickle_pairs)
    assigned_k = assign_k_to_pairs(pairs, k)
    pickle_results(assigned_k, pickle_k)


main(pickle_pairs, pickle_k, k)
