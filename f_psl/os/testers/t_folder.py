from f_psl.os.generators.g_folder import GenFolder, Folder


drive = 'd'


def test_create_test() -> None:
    """
    ========================================================================
     Test the create_test() method.
    ========================================================================
    """
    folder = GenFolder.create_test(drive=drive)
    path = folder.path
    files = folder.filepaths()
    Folder.delete(path=folder.path)
    assert path == f'{drive}:\\temp\\test'
    assert files == [f'{path}\\test_1.txt', f'{path}\\test_2.txt']
