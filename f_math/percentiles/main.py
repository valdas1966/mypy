from typing import Iterable
import numpy as np


class UPercentiles:
    """
    ============================================================================
     Utility class for calculating percentiles.
    ============================================================================
    """

    from typing import Iterable
import numpy as np


class UPercentiles:
    """
    ============================================================================
     Utility class for calculating percentile-based integer bins.
    ============================================================================
    """

    @staticmethod
    def get_percentile_bins(values: Iterable[int],
                            n_bins: int) -> list[tuple[int, int]]:
        """
        ========================================================================
         Return percentile-based integer bin boundaries.

         n_bins is interpreted as the *percent step per bin*.
         For example:
            values = [1, 2, 3, 4]
            n_bins = 50  # 0–50%, 50–100%
            Return -> [(1, 3), (3, 5)]  # [1,3) and [3,5)
        ========================================================================
        """
        li = list(values)
        if not li:
            return []

        if n_bins <= 0 or n_bins > 100 or 100 % n_bins != 0:
            raise ValueError(
                f"n_bins must be a positive divisor of 100 (got {n_bins})."
            )

        arr = np.array(li, dtype=float)

        # Percentile points: 0, n_bins, 2*n_bins, ..., 100
        percent_points = np.arange(0, 101, n_bins)
        percentiles = np.percentile(arr, percent_points)

        # Build integer boundaries:
        # - first = min value
        # - intermediate = ceil of internal percentiles
        # - last = max value + 1
        boundaries: list[int] = []

        min_val = int(min(li))
        max_val = int(max(li))

        boundaries.append(min_val)
        for p in percentiles[1:-1]:
            boundaries.append(int(np.ceil(p)))
        boundaries.append(max_val + 1)

        # Create bins as (start, end) pairs
        bins: list[tuple[int, int]] = [
            (boundaries[i], boundaries[i + 1])
            for i in range(len(boundaries) - 1)
        ]
        return bins
