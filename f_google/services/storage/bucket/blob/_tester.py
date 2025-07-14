from f_google.services.storage import Storage
from f_google.services.storage.bucket import Bucket
from f_google.services.storage.bucket.blob import Blob


def test_blob() -> None:
    """
    ========================================================================
     Test Blob creation using factory methods.
    ========================================================================
    """
    storage: Storage = Storage.Factory.rami()
    bucket: Bucket = storage['noteret_mp4']
