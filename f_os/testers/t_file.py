from f_os.u_file import UFile


def test_create_delete():
    path = 'g:\\test'
    UFile.create(path)
    assert UFile.is_exists(path)
    UFile.delete(path)
    assert not UFile.is_exists(path)


def test_change_extension():
    path_py = 'g:\\test.py'
    path_csv = 'g:\\test.csv'
    UFile.create(path_py)
    UFile.delete(path_csv)
    UFile.change_extension(path_py, extension_new='csv')
    assert UFile.is_exists(path_csv)
    UFile.delete(path_csv)
