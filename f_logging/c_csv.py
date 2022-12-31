from f_abstract.inittable import Inittable
from f_utils import u_csv
from f_utils import u_datetime
from f_utils import u_dict


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

    # Inittable
    def _init_run_funcs(self) -> None:
        self._set_path()
        self._create()

    def append_list(self, row: list) -> None:
        """
        ========================================================================
         Description: Append New-Log-Row.
        ========================================================================
        """
        u_csv.append(path=self._path, row=row)

    def append_dict(self, d: dict) -> None:
        """
        ========================================================================
         Desc: Append New-Log Row by matching the Header with the Dict-Keys.
        ========================================================================
        """
        row = u_dict.get_ordered_values(d=d, keys_order=self._header)
        self.append_list(row=row)

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
