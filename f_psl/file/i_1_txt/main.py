from f_psl.file.i_0_base.main import FileBase


class FileTxt(FileBase):
    """
    ========================================================================
     Text file with read/write content operations.
    ========================================================================
    """

    # Factory
    Factory: type = None

    @property
    def text(self) -> str:
        """
        ====================================================================
         Return the file content as string.
        ====================================================================
        """
        return self._path.read_text()

    @text.setter
    def text(self, value: str) -> None:
        """
        ====================================================================
         Write text to the file (overwrites).
        ====================================================================
        """
        self._path.write_text(value)

    def lines(self) -> list[str]:
        """
        ====================================================================
         Return the file content as list of lines.
        ====================================================================
        """
        return self.text.splitlines()

    def write_line(self, line: str, index: int = -1) -> None:
        """
        ====================================================================
         Insert a line at the given index. Default appends at end.
        ====================================================================
        """
        ls = self.lines()
        if index == -1:
            ls.append(line)
        else:
            ls.insert(index, line)
        self.text = '\n'.join(ls)

    def delete_line(self, index: int) -> None:
        """
        ====================================================================
         Delete a line at the given index.
        ====================================================================
        """
        ls = self.lines()
        ls.pop(index)
        self.text = '\n'.join(ls)
