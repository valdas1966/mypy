from f_psl.os.generators.g_path import GenPath
from f_psl.os.u_path import UPath


def test_last_folder() -> None:
    """
    ============================================================================
     Test the last_folder method.
    ============================================================================
    """
    path = GenPath.multiple_folders()
    assert UPath.last_folder(path) == 'folder_last'


def test_filename() -> None:
    """
    ============================================================================
     Test the filename method.
    ============================================================================
    """
    path = 'c:\\folder_1\\folder_2\\file_name.txt'
    assert UPath.filename(path) == 'file_name.txt'
    assert UPath.filename(path, with_domain=False) == 'file_name'
