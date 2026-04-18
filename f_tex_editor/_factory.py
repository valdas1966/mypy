from f_tex import Tex

from f_tex_editor.main import TexEditor


class Factory:
    """
    ============================================================================
     Factory for TexEditor.
    ============================================================================
    """

    @staticmethod
    def a() -> TexEditor:
        """
        ========================================================================
         Default TexEditor backed by a tectonic Tex compiler.
        ========================================================================
        """
        return TexEditor(tex=Tex.Factory.a())
