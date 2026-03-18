from f_google.services.drive import Drive
import os
import pytest
import tempfile
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


def test_upload_file(drive: Drive, test_folder: str) -> None:
    """
    ========================================================================
     Test upload() uploads a single file to Drive.
    ========================================================================
    """
    with tempfile.NamedTemporaryFile(suffix='.txt',
                                     delete=False) as f:
        f.write(b'hello drive')
        path_local = f.name
    try:
        path_drive = f'{test_folder}/uploaded.txt'
        drive.upload(path_src=path_local, path_dest=path_drive)
        assert drive.is_exists(path=path_drive)
    finally:
        os.remove(path_local)


def test_download_file(drive: Drive, test_folder: str) -> None:
    """
    ========================================================================
     Test download() downloads a file from Drive to local.
    ========================================================================
    """
    # Upload a file first
    with tempfile.NamedTemporaryFile(suffix='.txt',
                                     delete=False) as f:
        f.write(b'download me')
        path_local = f.name
    try:
        path_drive = f'{test_folder}/to_download.txt'
        drive.upload(path_src=path_local, path_dest=path_drive)
    finally:
        os.remove(path_local)
    # Download it
    with tempfile.TemporaryDirectory() as tmp:
        path_dest = os.path.join(tmp, 'to_download.txt')
        drive.download(path_src=path_drive,
                       path_dest=path_dest)
        assert os.path.isfile(path_dest)
        with open(path_dest, 'rb') as f:
            assert f.read() == b'download me'


def test_upload_overwrite(drive: Drive,
                          test_folder: str) -> None:
    """
    ========================================================================
     Test upload() overwrites an existing file silently.
    ========================================================================
    """
    with tempfile.NamedTemporaryFile(suffix='.txt',
                                     delete=False) as f:
        f.write(b'version 1')
        path_local = f.name
    try:
        path_drive = f'{test_folder}/overwrite.txt'
        drive.upload(path_src=path_local, path_dest=path_drive)
    finally:
        os.remove(path_local)
    # Overwrite with new content
    with tempfile.NamedTemporaryFile(suffix='.txt',
                                     delete=False) as f:
        f.write(b'version 2')
        path_local = f.name
    try:
        drive.upload(path_src=path_local, path_dest=path_drive)
    finally:
        os.remove(path_local)
    # Download and verify new content
    with tempfile.TemporaryDirectory() as tmp:
        path_dest = os.path.join(tmp, 'overwrite.txt')
        drive.download(path_src=path_drive,
                       path_dest=path_dest)
        with open(path_dest, 'rb') as f:
            assert f.read() == b'version 2'


def test_upload_creates_parents(drive: Drive,
                                test_folder: str) -> None:
    """
    ========================================================================
     Test upload() creates parent folders on Drive if needed.
    ========================================================================
    """
    with tempfile.NamedTemporaryFile(suffix='.txt',
                                     delete=False) as f:
        f.write(b'deep file')
        path_local = f.name
    try:
        path_drive = (f'{test_folder}/auto_parent'
                      f'/deep/file.txt')
        drive.upload(path_src=path_local,
                     path_dest=path_drive)
        assert drive.is_exists(path=path_drive)
    finally:
        os.remove(path_local)


def test_upload_folder(drive: Drive,
                       test_folder: str) -> None:
    """
    ========================================================================
     Test upload() uploads a folder recursively to Drive.
    ========================================================================
    """
    with tempfile.TemporaryDirectory() as tmp:
        # Create local folder structure
        os.makedirs(os.path.join(tmp, 'sub'))
        with open(os.path.join(tmp, 'a.txt'), 'w') as f:
            f.write('file a')
        with open(os.path.join(tmp, 'sub', 'b.txt'), 'w') as f:
            f.write('file b')
        path_drive = f'{test_folder}/uploaded_folder'
        drive.upload(path_src=tmp, path_dest=path_drive)
    assert drive.is_exists(path=path_drive)
    assert 'a.txt' in drive.files(path=path_drive)
    assert 'sub' in drive.folders(path=path_drive)
    assert 'b.txt' in drive.files(
        path=f'{path_drive}/sub'
    )


def test_download_folder(drive: Drive,
                         test_folder: str) -> None:
    """
    ========================================================================
     Test download() downloads a folder recursively to local.
    ========================================================================
    """
    # Upload a folder first
    with tempfile.TemporaryDirectory() as tmp:
        os.makedirs(os.path.join(tmp, 'child'))
        with open(os.path.join(tmp, 'x.txt'), 'w') as f:
            f.write('file x')
        with open(os.path.join(tmp, 'child', 'y.txt'),
                  'w') as f:
            f.write('file y')
        path_drive = f'{test_folder}/folder_to_dl'
        drive.upload(path_src=tmp, path_dest=path_drive)
    # Download the folder
    with tempfile.TemporaryDirectory() as tmp:
        path_dest = os.path.join(tmp, 'folder_to_dl')
        drive.download(path_src=path_drive,
                       path_dest=path_dest)
        assert os.path.isdir(path_dest)
        assert os.path.isfile(
            os.path.join(path_dest, 'x.txt')
        )
        assert os.path.isdir(
            os.path.join(path_dest, 'child')
        )
        assert os.path.isfile(
            os.path.join(path_dest, 'child', 'y.txt')
        )
        with open(os.path.join(path_dest, 'x.txt')) as f:
            assert f.read() == 'file x'
        with open(os.path.join(path_dest, 'child',
                               'y.txt')) as f:
            assert f.read() == 'file y'
