from f_google.services.storage import Storage, Bucket


def test_bucket() -> None:
    """
    ========================================================================
     Test bucket creation using factory methods.
    ========================================================================
    """
    storage = Storage.Factory.rami()
    bucket_valid: Bucket = storage.bucket('noteret_mp4')
    assert bucket_valid
    assert bucket_valid.name == 'noteret_mp4'
    bucket_invalid: Bucket = storage.bucket('noteret_mp4_invalid')
    assert not bucket_invalid
    