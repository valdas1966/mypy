from f_log.utils import set_debug, log_2
from f_math.percentiles.utils import UPercentiles
from f_ds.pair import Pair
from f_utils import u_pickle


@log_2
def load_pairs(pickle_pairs: str) -> dict[str, list[Pair]]:
    """
    ============================================================================
     Load the pairs from the pickle file.
    ============================================================================
    """
    return u_pickle.load(path=pickle_pairs)


@log_2
def generate_percentiles_for_grids(pairs: dict[str, list[Pair]],
                                   n_bins: int) -> dict[str, dict[int, list[Pair]]]:
    """
    ============================================================================
     Generate Percentile-Based Pairs for a List of Grids.
    ============================================================================
    """
    @log_2
    def for_grid(name: str, pairs: list[Pair], i: int) -> dict[int, list[Pair]]:
        """
        ========================================================================
         Generate Percentile-Based Pairs for a given Grid.
        ========================================================================
        """
        # Calculate distances for all pairs
        distances: list[int] = [pair.a.distance(other=pair.b) for pair in pairs]

        # Get percentile bins
        bins = UPercentiles.get_bins(values=distances, n_bins=n_bins)

        # Collect pairs for each percentile bin
        percentiles: dict[int, list[Pair]] = dict()
        for bin in bins:
            percentiles[bin.percentile] = list()
            for pair, distance in zip(pairs, distances):
                if distance in bin:
                    percentiles[bin.percentile].append(pair)

        return percentiles

    d: dict[str, dict[int, list[Pair]]] = dict()
    for i, (name, grid_pairs) in enumerate(pairs.items()):
        percentiles = for_grid(name=name, pairs=grid_pairs, i=i+1)
        d[name] = percentiles
    return d


@log_2
def percentiles_to_pickle(percentiles: dict[str, dict[int, list[Pair]]],
                          pickle_percentiles: str) -> None:
    """
    ========================================================================
     Pickle the dict[Grid.Name, dict[Percentile, List[Pair]]] to the given path.
    ========================================================================
    """
    u_pickle.dump(obj=percentiles, path=pickle_percentiles)


"""
===============================================================================
 Main - Generate Percentile-Based Pairs for a List of Grids.
-------------------------------------------------------------------------------
 Input: Pickle of dict[Grid.Name, List[Pair]].
 Output: Pickle of dict[Grid.Name, dict[Percentile, List[Pair]]].
===============================================================================
"""

set_debug(enabled=True, path='percentiles.log')
pickle_pairs = 'f:\\paper\\i_2_pairs\\pairs.pkl'
pickle_percentiles = 'f:\\paper\\i_3_percentiles\\percentiles.pkl'
n_bins = 10

@log_2
def main(pickle_pairs: str, pickle_percentiles: str) -> None:
    """
    ========================================================================
     Main
    ========================================================================
    """
    pairs = load_pairs(pickle_pairs=pickle_pairs)
    percentiles = generate_percentiles_for_grids(pairs=pairs, n_bins=n_bins)
    percentiles_to_pickle(percentiles, pickle_percentiles)

main(pickle_pairs, pickle_percentiles=pickle_percentiles)
