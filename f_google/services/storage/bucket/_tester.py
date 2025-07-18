from f_google.services.storage import Storage, Bucket


def test_bucket() -> None:
    """
    ========================================================================
     Test bucket creation using factory methods.
    ========================================================================
    """
    storage = Storage.Factory.rami()
    bucket_valid: Bucket = storage.get_bucket('noteret_mp4')
    assert bucket_valid
    assert bucket_valid.name == 'noteret_mp4'
    bucket_invalid: Bucket = storage.get_bucket('noteret_mp4_invalid')
    print(type(bucket_invalid))
    