import os


class UPath:
    """
    ============================================================================
     Utils for Paths using os.path
    ============================================================================
    """

    @staticmethod
    def last_folder(path: str) -> str:
        """
        ========================================================================
         Return the last folder of the path.
        ========================================================================
        """
        return os.path.basename(os.path.dirname(path))