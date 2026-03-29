from typing import Callable

# Type alias for Phi aggregation functions
PhiFunc = Callable[[list[int], list[int]], int]


class UPhi:
    """
    ============================================================================
     Static Utility for Heuristic Aggregation Functions (Phi).
    ============================================================================
    """

    @staticmethod
    def min(h_vec: list[int], active: list[int]) -> int:
        """
        ========================================================================
         Return the Minimum heuristic value among active goals.
        ========================================================================
        """
        return min(h_vec[i] for i in active)

    @staticmethod
    def max(h_vec: list[int], active: list[int]) -> int:
        """
        ========================================================================
         Return the Maximum heuristic value among active goals.
        ========================================================================
        """
        return max(h_vec[i] for i in active)

    @staticmethod
    def mean(h_vec: list[int], active: list[int]) -> int:
        """
        ========================================================================
         Return the Mean heuristic value among active goals (floored).
        ========================================================================
        """
        return sum(h_vec[i] for i in active) // len(active)
