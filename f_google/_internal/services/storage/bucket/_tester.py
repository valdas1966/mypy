from . import Bucket


def test_bucket() -> None:
    """
    ========================================================================
     Test Bucket creation using factory methods.
    ========================================================================
    """
    bucket = Bucket.Factory.noteret_mp4()
    assert bucket.name == 'noteret_mp4'
