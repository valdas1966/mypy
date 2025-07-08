from f_core.mixins.has.name import HasName


class FileKey(HasName):
    """
    ============================================================================
     Class for Keys stored in Files.
    ============================================================================
    """

    _vars = 'c:\\vars'
    _d = {'TIKTOK': f'{_vars}\\tiktok no watermark.txt'}

    def __init__(self, name: str) -> None:
        """
        ========================================================================
         Init private Attributes.
        ========================================================================
        """
        HasName.__init__(self, name)

    def to_str(self) -> str:
        """
        ========================================================================
         Return a String-Key.
        ========================================================================
        """
        return self._d[self.name]
