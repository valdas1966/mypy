from f_utils.psl.os.folder import Folder
from f_file.txt import Txt


class GenFolder:
    """
    ========================================================================
     Generator for Folder objects.
    ========================================================================
    """

    @staticmethod
    def create_test(drive: str = 'g') -> Folder:
        """
        ====================================================================
         Create a test folder.
        ====================================================================
        """
        path_folder = f'{drive}:\\temp\\test'
        path_file_1 = f'{drive}:\\temp\\test\\test_1.txt'
        path_file_2 = f'{drive}:\\temp\\test\\test_2.txt'
        folder = Folder.create(path=path_folder)
        Txt.create(path=path_file_1)
        Txt.create(path=path_file_2)
        return folder
