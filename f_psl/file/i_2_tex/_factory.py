import tempfile
import os
from f_psl.file.i_2_tex.main import FileTex


class Factory:
    """
    ========================================================================
     Factory for FileTex.
    ========================================================================
    """

    @staticmethod
    def empty() -> FileTex:
        """
        ====================================================================
         Create an empty FileTex.
        ====================================================================
        """
        path = os.path.join(tempfile.gettempdir(),
                            'empty.tex')
        return FileTex(path=path)

    @staticmethod
    def article() -> FileTex:
        """
        ====================================================================
         Create a minimal article FileTex.
        ====================================================================
        """
        path = os.path.join(tempfile.gettempdir(),
                            'article.tex')
        f = FileTex(path=path)
        f.text = '\\documentclass{article}\n\\begin{document}\n\\end{document}'
        return f
