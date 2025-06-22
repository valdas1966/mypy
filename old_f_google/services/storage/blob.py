
class Blob:
    """
    ============================================================================
     Static-Methods for list BLOB-Object in the Google-Storage.
    ============================================================================
    """

    @staticmethod
    def is_folder(name: str) -> bool:
        """
        ========================================================================
         Return True if the Folder-Name represents list Folder.
        ========================================================================
        """
        return name.endswith('/')
