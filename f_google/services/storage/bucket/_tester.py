from f_google.services.storage import Storage, Bucket


def test_bucket() -> None:
    """
    ========================================================================
     Test Bucket creation using factory methods.
    ========================================================================
    """
    storage: Storage = Storage.Factory.rami()
    bucket: Bucket = storage['noteret_mp4']
    assert bucket.name == 'noteret_mp4'
