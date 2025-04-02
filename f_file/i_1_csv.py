from f_file.i_0_base import FileBase


class CSV(FileBase[list[str]]):
    """
    ============================================================================
     CSV-File.
    ============================================================================
    """

    def __init__(self,
                 path: str,
                 delimiter: str = ',',
                 titles: list[str] = None) -> None:
        """
        ========================================================================
         Initialize the CSV object.
        ========================================================================
        """
        self._delimiter = delimiter
        self._titles = titles if titles else list()
        super().__init__(path=path)

    def write_line(self, line: list[str]) -> None:
        """
        ========================================================================
         Convert a Line into a str with delimiter and write it to the File.
        ========================================================================
        """
        str_line = self._delimiter.join(line)
        super().write_line(str_line)

    def _read_lines(self) -> list[list[str]]:
        """
        ========================================================================
         Read the Titles and the Lines from the File.
        ========================================================================
        """
        with open(self._path, 'r') as file:
            lines = file.readlines()
            self._titles = lines[0].split(self._delimiter)
            self._lines = [line.split(self._delimiter) for line in lines[1:]]
