from f_psl.pathlib import u_pathlib


def test_to_path() -> None:
    """
    ========================================================================
     Test the to_path() method.
    ========================================================================
    """
    path = u_pathlib.to_path('folder/file.txt')
    assert path == '/Users/eyalberkovich/folder/file.txt'
