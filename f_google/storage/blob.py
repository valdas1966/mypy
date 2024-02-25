
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

    @staticmethod
    def to_folder_format(name: str) -> str:
        """
        ========================================================================
         Format the Name into Folder-Name Format.
        ========================================================================
        """
        if not name or Blob.is_folder(name=name):
            return name
        else:
            return name + '/'
