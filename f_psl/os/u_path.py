import os


class UPath:
    """
    ============================================================================
     Utils for Paths using os.old_path
    ============================================================================
    """

    @staticmethod
    def last_folder(path: str) -> str:
        """
        ========================================================================
         Return the last folder of the old_path.
        ========================================================================
        """
        return os.path.basename(os.path.dirname(path))