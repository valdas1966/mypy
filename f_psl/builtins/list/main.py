
class UList:
    """
    ============================================================================
     Class for List-related utilities.
    ============================================================================
    """

    @staticmethod
    def sliding_windows(li: list, size: int) -> list[list]:
        """
        ========================================================================
         Return all Sliding-Windows of the given Size over the List, in
          order.
         * Example: sliding_windows(li=[1, 2, 3], size=2) -> [[1, 2],
            [2, 3]].
         * For a List of length N and Window-Size K (with K >= 1), returns
            N - K + 1 windows; returns [] when K > N.
        ========================================================================
        """
        return [li[i:i + size] for i in range(len(li) - size + 1)]
