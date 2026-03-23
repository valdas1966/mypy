from f_overleaf import OverLeaf
from f_overleaf.project import ProjectOverLeaf
import pytest


@pytest.fixture(scope='module')
def project() -> ProjectOverLeaf:
    """
    ========================================================================
     Return the 'Test' project from Valdas's OverLeaf.
    ========================================================================
    """
    return OverLeaf.Factory.valdas()['Test']


def test_key(project: ProjectOverLeaf) -> None:
    """
    ========================================================================
     Test that key is a non-empty string.
    ========================================================================
    """
    assert isinstance(project.key, str)
    assert len(project.key) > 0


def test_name(project: ProjectOverLeaf) -> None:
    """
    ========================================================================
     Test that name is 'Test'.
    ========================================================================
    """
    assert project.name == 'Test'


def test_list_files(project: ProjectOverLeaf) -> None:
    """
    ========================================================================
     Test that list_files() returns a list of strings.
    ========================================================================
    """
    files = project.list_files()
    assert isinstance(files, list)
    assert all(isinstance(f, str) for f in files)
    assert 'main.tex' in files


def test_list_folders(project: ProjectOverLeaf) -> None:
    """
    ========================================================================
     Test that list_folders() returns a list of strings.
    ========================================================================
    """
    folders = project.list_folders()
    assert isinstance(folders, list)
    assert all(isinstance(f, str) for f in folders)


def test_create_and_delete_folder(project: ProjectOverLeaf) -> None:
    """
    ========================================================================
     Test create_folder() and delete_folder().
    ========================================================================
    """
    name = '_test_folder'
    # Create
    project.create_folder(path=name)
    assert name in project.list_folders()
    # Override (should not raise)
    project.create_folder(path=name)
    assert name in project.list_folders()
    # Delete
    project.delete_folder(path=name)
    assert name not in project.list_folders()


def test_create_and_delete_file(project: ProjectOverLeaf) -> None:
    """
    ========================================================================
     Test create_file() and delete_file().
    ========================================================================
    """
    name = '_test_file.tex'
    # Create
    project.create_file(path=name, text='hello')
    assert name in project.list_files()
    # Override (should not raise)
    project.create_file(path=name, text='world')
    assert name in project.list_files()
    # Delete
    project.delete_file(path=name)
    assert name not in project.list_files()
