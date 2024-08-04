
class Indexes:
    """
    ============================================================================
     Utils-Class to return Indexes of the given String based on a given
      conditions.
    ============================================================================
    """

    @staticmethod
    def of(s: str,
           exceptions: set[str] = None) -> list[int]:
        """
        ========================================================================
         Return list[int] of Indexes of the given String without exceptions.
        ========================================================================
        """
        if exceptions is None:
            return list(range(len(s)))
        return [i for i, ch in s if ch not in exceptions]
