from f_google.services.storage.bucket.blob.main import Blob
from google.cloud.storage.bucket import Bucket as GBucket
from f_ds.mixins.collectionable import Collectionable
from f_core.mixins.has.name import HasName


class Bucket(HasName, Collectionable):
    """
    ============================================================================
     Wrapper for Google-Cloud-Storage Bucket.
    ============================================================================
    """

    def __init__(self, g_bucket: GBucket) -> None:
        """
        ========================================================================
         Init private Attributes.
        ========================================================================
        """
        self._g_bucket = g_bucket
        HasName.__init__(self, name=g_bucket.name)

    def to_iterable(self) -> list[Blob]:
        """
        ========================================================================
         Return List of Blobs in the Bucket.
        ========================================================================
        """
        return [Blob(g_blob=g_blob)
                for g_blob
                in self._g_bucket.list_blobs()]

    def names_blobs(self) -> list[str]:
        """
        ========================================================================
         Get names of all blobs in the bucket.
        ========================================================================
        """
        return [blob.name for blob in self._g_bucket.list_blobs()]

    def __getitem__(self, name: str) -> Blob:
        """
        ========================================================================
         Get Blob by name.
        ========================================================================
        """
        g_blob = self._g_bucket.blob(name)
        return Blob(g_blob=g_blob)

    