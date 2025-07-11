from f_google._internal.services.storage.main import Storage, Bucket


class Factory:
    """
    ============================================================================
     Factory for Google-Cloud-Storage Bucket.
    ============================================================================
    """

    @staticmethod
    def noteret_mp4() -> Bucket:
        storage = Storage.Factory.rami()
        return storage['noteret_mp4']
