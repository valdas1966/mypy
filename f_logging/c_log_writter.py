from f_core.inittable import Inittable


class LogWritter(Inittable):
    """
    ============================================================================
     Desc: Write Logs into Small files by list given threshold of lines.
    ============================================================================
     Attributes:
    ----------------------------------------------------------------------------
        1. nodes : str (Path of the Folder to store the new files).
        2. threshold : int (Number of lines per file).
    ============================================================================
    """

    def _init_add_atts(self) -> None:
        super()._init_add_atts()
        # [file] Opened File to Write
        self._file = None
        # [int] Index of Current File
        self._i_file = 0
        # [int] Index of Current Line
        self._i_row = 0

    def write(self, line: str) -> None:
        if not self._file:
            self._open_file()
        if not line[-1] == '\n':
            line += '\n'
        self._file.write(line)
        self._i_row += 1
        if self._i_row == self._threshold:
            self._i_file += 1
            self._i_row = 0
            self._file.close()
            self._file = None

    def close(self) -> None:
        if self._file:
            self._file.close()

    def _open_file(self) -> None:
        filepath = f'{self._folder}\\{self._i_file}.log'
        self._file = open(filepath, 'w')
