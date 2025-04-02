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
        super().__init__(path=path)
        if titles:
            self.write_titles(titles=titles)

    def write_lines(self,
                    lines: list[list[str]],
                    append: bool = False) -> None:
        """
        ========================================================================
         Write a list of lines to the file.
        ========================================================================
        """
        lines = [self._delimiter.join(line) + '\n' for line in lines]
        super().write_lines(lines=lines, append=append)
    
    def write_titles(self, titles: list[str]) -> None:
        """
        ========================================================================
         Write the titles to the file.
        ========================================================================
        """
        line = self._delimiter.join(titles) + '\n'
        super().write_lines(lines=[line], append=False)

    def read_lines(self) -> list[list[str]]:
        """
        ========================================================================
         Read the lines from the file.
        ========================================================================
        """ 
        lines = super().read_lines()
        if len(lines) <= 1:
            return list()
        lines = [line.split(self._delimiter) for line in lines[1:]]  
        return [line.strip() for line in lines]
    
    def read_titles(self) -> list[str]:
        """
        ========================================================================
         Read the titles from the file.
        ========================================================================
        """
        lines = super().read_lines()
        return lines[0].split(self._delimiter)
        