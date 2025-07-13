from f_google._internal.services.storage import Storage


def test_storage() -> None:
    """
    ========================================================================
     Test storage creation using factory methods.
    ========================================================================
    """
    storage = Storage.Factory.rami()
    assert storage


def test_getitem() -> None:
    """
    ========================================================================
     Test __getitem__() method.
    ========================================================================
    """
    storage = Storage.Factory.rami()
    bucket = storage['noteret_mp4']
    assert bucket.name == 'noteret_mp4'


def test_contains() -> None:
    """
    ========================================================================
     Test __contains__() method.
    ========================================================================
    """
    storage = Storage.Factory.rami()
    assert 'noteret_mp4' in storage
