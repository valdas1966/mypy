from f_math.percentiles.bin import Bin
from typing import Iterable
import numpy as np


class UPercentiles:
    """
    ============================================================================
     Utility class for calculating percentiles.
    ============================================================================
    """

    @staticmethod
    def get_bins(values: Iterable[int],
                 n_bins: int) -> list[Bin]:
        """
        ========================================================================
         Return percentile-based integer bin boundaries as Bin objects.

         n_bins is interpreted as the *percent step per bin*.
         For example:
            values = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
            n_bins = 50  # 0–50%, 50–100%

            Returns 2 bins:
            - Bin(percentile=50, lower=1, upper=6)   # [1,6) - lower 50%
            - Bin(percentile=100, lower=6, upper=11) # [6,11) - upper 50%
        ========================================================================
        """
        li_values: list[int] = list(values)

        arr_values: np.ndarray = np.array(li_values, dtype=float)

        # Percentile points: 0, n_bins, 2*n_bins, ..., 100
        percent_points = np.arange(0, 101, n_bins)
        percentiles = np.percentile(arr_values, percent_points)

        # Build integer boundaries:
        # - first = min value
        # - intermediate = ceil of internal percentiles
        # - last = max value + 1
        boundaries: list[int] = []

        min_val = int(min(li_values))
        max_val = int(max(li_values))

        boundaries.append(min_val)
        for p in percentiles[1:-1]:
            boundaries.append(int(np.ceil(p)))
        boundaries.append(max_val + 1)

        # Create bins with percentile labels
        bins: list[Bin] = []
        for i in range(len(boundaries) - 1):
            if boundaries[i] < boundaries[i + 1]:
                # The percentile represents the upper bound of this bin
                # e.g., first bin is 0-50%, labeled as 50
                percentile = percent_points[i + 1]
                bins.append(
                    Bin(percentile=int(percentile),
                        lower=boundaries[i],
                        upper=boundaries[i + 1])
                )
        return bins

 