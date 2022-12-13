from f_abstract.inittable import Inittable
from f_utils import u_csv
from f_utils import u_datetime


class CsvLogger(Inittable):

    # str [INIT] (CSV-Folder)
    _folder = None

    # str [INIT] (Logger-Name)
    _name = None

    # list[obj] [INIT] (Logger Column-Names)
    _header = None

    # str (CSV-Path)
    _path = None

    def __init__(self, **kwargs) -> None:
        """
        ========================================================================
         Description: Constructor. Set CSV-Path and Create Csv-File.
        ========================================================================
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
