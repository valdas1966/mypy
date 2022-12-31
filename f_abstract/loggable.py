from f_abstract.inittable import Inittable
from f_logging.c_csv import CsvLogger


class Loggable(Inittable):

    # Inittable
    def _init_add_atts(self) -> None:
        """
        ========================================================================
         Description: Add additional attributes to those in the init.
        ========================================================================
        """
        super()._init_add_atts()
        # bool : Print Logs on Screen
        if not hasattr(self, '_verbose'):
            self._verbose = True
        # str : Delimiter in Print-Logging
        self.__deli = ' | '
        # CsvLogger
        if not hasattr(self, '_logger_csv'):
            self._logger_csv = None

    def _create_logger_csv(self,
                           folder: str,
                           header: str,
                           name: str = ()) -> None:
        """
        ========================================================================
         Desc: Create CsvLogger for Logging.
        ========================================================================
        """
        self._logger_csv = CsvLogger(folder=folder,
                                     name=name,
                                     header=header)

    def _log(self, **kwargs) -> None:
        """
        ========================================================================
         Description: Log.
        ========================================================================
        """
        if self._verbose:
            values = (str(val) for val in kwargs.values())
            print(self.__deli.join(values))
        if self._logger_csv:
            adds = kwargs.pop('adds')
            kwargs.update(adds)
            self._logger_csv.append_dict(d=kwargs, )
