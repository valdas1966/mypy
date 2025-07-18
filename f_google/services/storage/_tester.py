from f_google.services.storage import Storage
import pytest


@pytest.fixture
def storage() -> Storage:
    """
    ========================================================================
     Fixture for storage instance.
    ========================================================================
    """
    return Storage.Factory.rami()


def test_storage(storage: Storage) -> None:
    """
    ========================================================================
     Test storage creation using factory methods.
    ========================================================================
    """
    assert storage


def test_names_buckets(storage: Storage) -> None:
    """
    ========================================================================
     Test names buckets.
    ========================================================================
    """
    assert 'noteret_mp4' in storage.names_buckets()


def test_create_bucket(storage: Storage) -> None:
    """
    ========================================================================
     Test create bucket.
    ========================================================================
    """
    name = 'noteret_test_202507181'
    if name in storage.names_buckets():
        storage.delete_bucket(name)
    bucket = storage.create_bucket(name)
    assert bucket
    assert name in storage.names_buckets()
    storage.delete_bucket(name)


def test_get_bucket(storage: Storage) -> None:
    """
    ========================================================================
     Test get bucket.
    ========================================================================
    """
    name = 'noteret_mp4'
    bucket = storage.get_bucket(name)
    assert bucket
    assert bucket.name == name
