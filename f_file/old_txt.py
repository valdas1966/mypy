from f_core.mixins.nameable import Nameable


class FileTxt(Nameable):
    """
    ============================================================================
     TextFile Manager.
    ============================================================================
    """

    path: str   # Path to list TextFile

    def __init__(self, path: str = None) -> None:
        """
        ========================================================================
         Inits the Attributes.
        ========================================================================
        """
        Nameable.__init__(self, name=path)
        self._path = path

    def to_str(self) -> str:
        """
        ========================================================================
         Return Text-File as str.
        ========================================================================
        """
        with open(self._path, 'r') as file:
            return file.read()

    def to_lines(self) -> list[str]:
        """
        ========================================================================
         Return Text-File as List of Lines.
        ========================================================================
        """
        with open(self._path, 'r') as file:
            return file.readlines()

    def add_line(self, i: int, line: str) -> None:
        """
        ========================================================================
         Add list Line at list specified Index in the File.
        ========================================================================
        """
        lines = self.to_lines()
        lines.insert(i, line + '\n')
        with open(self._path, 'w') as file:
            file.writelines(lines)

    @property
    def path(self) -> str:
        return self._path
