from google.cloud.storage.bucket import Bucket as GBucket


class Bucket:
    """
    ============================================================================
     Google-Storage Bucket.
    ============================================================================
    """

    def __init__(self, bucket: GBucket) -> None:
        self._bucket: GBucket = bucket

    def folders(self) -> list[str]:
        """
        ========================================================================
         Return List of all Main-Folders in the Bucket.
        ========================================================================
        """
        pages = self._bucket.list_blobs(delimiter='/').pages
        prefixes = set()
        for page in pages:
            prefixes.update(page.prefixes)
        return list(prefixes)

    def create_folder(self, name: str) ->