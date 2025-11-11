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

    
    @staticmethod
    def filename(path: str, with_domain: bool = True) -> str:
        """
        ========================================================================
         Return the filename of the path.
        ========================================================================
        """
        if with_domain:
            return os.path.basename(path)
        else:
            return os.path.basename(path).split('.')[0]
