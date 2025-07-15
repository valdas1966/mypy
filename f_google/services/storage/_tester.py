from f_google.services.storage import Storage


def test_storage() -> None:
    """
    ========================================================================
     Test storage creation using factory methods.
    ========================================================================
    """
    storage = Storage.Factory.rami()
    assert storage


def test_bucket() -> None:
    """
    ========================================================================
     Test bucket creation using factory methods.
    ========================================================================
    """
    storage = Storage.Factory.rami()
    bucket_valid = storage.bucket('noteret_mp4')
    assert bucket_valid is not None
    assert bucket_valid.name == 'noteret_mp4'
    bucket_invalid = storage.bucket('noteret_mp4_invalid')
    assert bucket_invalid is None
