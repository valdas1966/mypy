import tempfile
import os
from f_psl.file.i_0_base.main import FileBase


class Factory:
    """
    ========================================================================
     Factory for FileBase.
    ========================================================================
    """

    @staticmethod
    def empty() -> FileBase:
        """
        ====================================================================
         Create a FileBase with a new empty temp file.
        ====================================================================
        """
        path = os.path.join(tempfile.gettempdir(),
                            'empty.tmp')
        return FileBase(path=path)

    @staticmethod
    def hello() -> FileBase:
        """
        ====================================================================
         Create a FileBase with a temp file containing 'hello'.
        ====================================================================
        """
        path = os.path.join(tempfile.gettempdir(),
                            'hello.txt')
        with open(path, 'w') as f:
            f.write('hello')
        return FileBase(path=path)
