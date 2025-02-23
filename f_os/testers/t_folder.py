from f_os.generators.g_folder import GenFolder, Folder


def test_create_test() -> None:
    """
    ========================================================================
     Test the create_test() method.
    ========================================================================
    """
    folder = GenFolder.create_test()
    path = folder.path
    files = folder.files()
    Folder.delete(path=folder.path)
    assert path == 'g:\\temp\\test'
    assert files == ['test_1.txt', 'test_2.txt']
