from f_abstract.inittable import Inittable
from f_utils import u_csv
from f_utils import u_datetime


class CsvLogger(Inittable):
    """
    ==================================================================================
     Desc: Write Logs into CSV-File.
    ==================================================================================
     Attributes:
    ----------------------------------------------------------------------------------
        1. _folder : str (CSV-Folder).
        2. _name : str (Logger-Name).
        3. _header : list (Column-Names).
    ==================================================================================
    """



    def __init__(self, **kwargs) -> None:
        """
        ========================================================================
         Desc: Set CSV-Path by datetime and Create Csv-File by the path.
        ========================================================================
         Attributes:
        ------------------------------------------------------------------------
            1. _folder : str (CSV-Folder).
            2. _name : str (Logger-Name).
            3. _header : list (Column-Names).
        =========================================================================
        """
        super().__init__(**kwargs)
        self._set_path()
        self._create()

    def append(self, row: 'list of obj') -> None:
        """
        ========================================================================
         Description: Append New-Log-Row.
        ========================================================================
        """
        u_csv.append(path=self._path, row=row)

    def _set_path(self) -> None:
        """
        ========================================================================
         Description: Set Csv-Path.
        ========================================================================
        """
        if not self._name:
            self._name = str()
        dt = u_datetime.now(format='NUM')
        self._path = f'{self._folder}\\{dt}{self._name}.csv'

    def _create(self) -> None:
        """
        ========================================================================
         Description: Create Csv-Logger-File.
        ========================================================================
        """
        u_csv.create(path=self._path, header=self._header)
