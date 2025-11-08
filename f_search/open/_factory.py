from f_search.open.main import Open, QueuePriority


class Factory:
    """
    ============================================================================
     Factory for creating Open objects.
    ============================================================================
    """

    @staticmethod
    def priority() -> Open[str, int]:
        """
        ========================================================================
         Generate an Open List with the 'A' and 'B' items,
          and descending order of priorities.
        ========================================================================
        """
        open = Open[str, int]()
        open.push(item='A', priority=2)
        open.push(item='B', priority=1)
        return open
