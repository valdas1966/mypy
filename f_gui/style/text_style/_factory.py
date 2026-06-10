from f_gui.style.text_style.main import TextStyle


class Factory:
    """
    ========================================================================
     Factory for TextStyle objects.
    ========================================================================
    """

    @staticmethod
    def default() -> TextStyle:
        """
        ========================================================================
         Generate the default TextStyle (monospace, 12px, not bold, no color).
        ========================================================================
         Matches the renderer's historical baseline text appearance.
        ========================================================================
        """
        return TextStyle()

    @staticmethod
    def title() -> TextStyle:
        """
        ========================================================================
         Generate a title TextStyle (larger, bold).
        ========================================================================
        """
        return TextStyle(size=18, bold=True)

    @staticmethod
    def body() -> TextStyle:
        """
        ========================================================================
         Generate a body TextStyle (sans-serif, 14px).
        ========================================================================
        """
        return TextStyle(font='sans-serif', size=14)

    @staticmethod
    def code() -> TextStyle:
        """
        ========================================================================
         Generate a code TextStyle (monospace, 12px) — the default look.
        ========================================================================
        """
        return TextStyle(font='monospace', size=12)
