from f_os.folder import Folder
from f_file.txt import Txt


class GenFolder:
    """
    ========================================================================
     Generator for Folder objects.
    ========================================================================
    """

    @staticmethod
    def create_test() -> Folder:
        """
        ====================================================================
         Create a test folder.
        ====================================================================
        """
        path_folder = 'g:\\temp\\test'
        path_file_1 = 'g:\\temp\\test\\test_1.txt'
        path_file_2 = 'g:\\temp\\test\\test_2.txt'
        folder = Folder.create(path=path_folder)
        Txt.create(path=path_file_1)
        Txt.create(path=path_file_2)
        return folder
