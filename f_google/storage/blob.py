
class Blob:
    """
    ============================================================================
     Static-Methods for a BLOB-Object in the Google-Storage.
    ============================================================================
    """

    @staticmethod
    def is_folder(name: str) -> bool:
        """
        ========================================================================
         Return True if the Folder-Name represents a Folder.
        ========================================================================
        """
        return name.endswith('/')
