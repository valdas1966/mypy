import tempfile
import os
from f_psl.file.i_1_txt.main import FileTxt


class Factory:
    """
    ========================================================================
     Factory for FileTxt.
    ========================================================================
    """

    @staticmethod
    def empty() -> FileTxt:
        """
        ====================================================================
         Create a FileTxt with a new empty temp file.
        ====================================================================
        """
        path = os.path.join(tempfile.gettempdir(),
                            'empty.txt')
        return FileTxt(path=path)

    @staticmethod
    def hello() -> FileTxt:
        """
        ====================================================================
         Create a FileTxt with 'hello' content.
        ====================================================================
        """
        path = os.path.join(tempfile.gettempdir(),
                            'hello.txt')
        f = FileTxt(path=path)
        f.text = 'hello'
        return f

    @staticmethod
    def lines() -> FileTxt:
        """
        ====================================================================
         Create a FileTxt with multi-line content.
        ====================================================================
        """
        path = os.path.join(tempfile.gettempdir(),
                            'lines.txt')
        f = FileTxt(path=path)
        f.text = 'aaa\nbbb\nccc'
        return f
