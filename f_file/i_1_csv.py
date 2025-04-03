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
        # Write new file
        if titles:
            self._titles = titles
            self.write_lines(lines=[titles], append=False)
        # Read existing file
        else:
            self._titles = self._read_titles()
        
    @property
    def titles(self) -> list[str]:
        """
        ========================================================================
         Get the titles of the CSV file.
        ========================================================================
        """
        return self._titles
    
    def write_lines(self,
                    lines: list[list[str]],
                    append: bool = True) -> None:
        """
        ========================================================================
         Write a list of lines to the file.
        ========================================================================
        """
        if not lines:
            return
        lines = [self._delimiter.join(line) for line in lines]
        super().write_lines(lines=lines, append=append)

    def write_dicts(self,
                    dicts: list[dict[str, str]],
                    append: bool = True) -> None:
        """
        ========================================================================
         Write a list of dictionaries to the file.
        ========================================================================
        """ 
        lines: list[list[str]] = list()
        for d in dicts:
            values = [str(d.get(title, str())) for title in self.titles]
            lines.append(values)
        self.write_lines(lines=lines, append=append)
    
    def read_lines(self, n: int = None) -> list[list[str]]:
        """
        ========================================================================
         Read the lines from the file.
        ========================================================================
        """ 
        # Read the lines, except the first line (titles)
        lines = super().read_lines(n=n)[1:]
        # Return empty list if no lines
        if not len(lines):
            return list()
        # Convert each line from string into list of strings
        lines = [line.split(self._delimiter) for line in lines]
        # Strip each string in each line from \n
        return [[value.strip() for value in line] for line in lines]
    
    def _read_titles(self) -> list[str]:
        """
        ========================================================================
         Read the titles from the file.
        ========================================================================
        """
        titles = super().read_lines(num_lines=1)[0]
        return titles.split(self._delimiter)
        