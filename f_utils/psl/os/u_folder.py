import os


class UFolder:
    """
    ============================================================================
     Utils for Folders using os Library.
    ============================================================================
    """

    @staticmethod
    def filepaths(path: str, recursive: bool = False) -> list[str]:
        """
        ========================================================================
         Return all filepaths in the given folder path with optional boolean
         argument to include all subfolders.
        ========================================================================
        """
        result = []
        with os.scandir(path) as it:
            for entry in it:
                if entry.is_file():
                    result.append(entry.path)
                elif entry.is_dir() and recursive:
                    result.extend(UFolder.filepaths(entry.path, recursive))
        return result
    