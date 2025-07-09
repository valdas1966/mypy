from .main import Storage


def test_storage() -> None:
    """
    ========================================================================
     Test storage creation using factory methods.
    ========================================================================
    """
    storage = Storage.Factory.rami()
    assert storage
