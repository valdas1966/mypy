from f_google.services.drive import Drive
import pytest
from uuid import uuid4


@pytest.fixture(scope='module')
def drive() -> Drive:
    """
    ========================================================================
     Create a Drive Client with VALDAS Credentials.
    ========================================================================
    """
    return Drive.Factory.valdas()


@pytest.fixture(scope='module')
def test_folder(drive) -> str:
    """
    ========================================================================
     Create a temporary test folder, yield its path, then delete it.
    ========================================================================
    """
    path = f'_test_{uuid4().hex[:8]}'
    drive.create_folder(path=path)
    yield path
    drive.delete(path=path)


def test_folders(drive: Drive, test_folder: str) -> None:
    """
    ========================================================================
     Test folders() returns created sub-folder names.
    ========================================================================
    """
    drive.create_folder(path=f'{test_folder}/sub_a')
    drive.create_folder(path=f'{test_folder}/sub_b')
    names = drive.folders(path=test_folder)
    assert 'sub_a' in names
    assert 'sub_b' in names


def test_files(drive: Drive, test_folder: str) -> None:
    """
    ========================================================================
     Test files() returns empty list when no files exist.
    ========================================================================
    """
    names = drive.files(path=test_folder)
    assert isinstance(names, list)


def test_is_exists(drive: Drive, test_folder: str) -> None:
    """
    ========================================================================
     Test is_exists() for existing and non-existing paths.
    ========================================================================
    """
    assert drive.is_exists(path=test_folder)
    assert not drive.is_exists(path=f'{test_folder}/nonexistent')


def test_create_folder(drive: Drive, test_folder: str) -> None:
    """
    ========================================================================
     Test create_folder() creates a nested folder.
    ========================================================================
    """
    path = f'{test_folder}/nested/deep'
    drive.create_folder(path=path)
    assert drive.is_exists(path=path)


def test_create_folder_override(drive: Drive,
                                test_folder: str) -> None:
    """
    ========================================================================
     Test create_folder() overrides an existing folder.
    ========================================================================
    """
    path = f'{test_folder}/override_me'
    drive.create_folder(path=path)
    drive.create_folder(path=f'{path}/child')
    # Override: should delete 'override_me' (and child) and re-create
    drive.create_folder(path=path)
    children = drive.folders(path=path)
    assert 'child' not in children


def test_delete(drive: Drive, test_folder: str) -> None:
    """
    ========================================================================
     Test delete() removes a folder.
    ========================================================================
    """
    path = f'{test_folder}/to_delete'
    drive.create_folder(path=path)
    assert drive.is_exists(path=path)
    drive.delete(path=path)
    assert not drive.is_exists(path=path)
