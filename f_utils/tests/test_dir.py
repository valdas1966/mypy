from f_utils import u_dir


def test_get_dir_name() -> None:
    path_dir = 'c:\\nodes\\sub_folder'
    result = u_dir.get_dir_name(path_dir=path_dir)
    expected = 'sub_folder'
    assert result == expected
