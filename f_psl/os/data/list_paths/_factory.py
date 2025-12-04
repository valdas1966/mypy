from f_psl.os.data.list_paths.main import ListPaths


class Factory:
    """
    ============================================================================
     Factory for creating ListPaths objects.
    ============================================================================
    """

    @staticmethod
    def ab() -> ListPaths:
        """
        ========================================================================
         Return a ListPaths object with the paths 'a' and 'b'.
        ========================================================================
        """
        paths = ['a', 'b']
        return ListPaths(paths=paths, name='AB')
    