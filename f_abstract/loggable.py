from f_abstract.inittable import Inittable
from f_logging.c_loguru import LoGuru
from f_utils import u_datetime


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
        # Loguru
        if not hasattr(self, '_loguru'):
            self._loguru = None
        # str : Delimiter in Print-Logging
        self.__deli = ' | '

    def _create_loguru(self,
                       folder: str,
                       name: str = ()) -> None:
        """
        ========================================================================
         Desc: Create LoGuru
        ========================================================================
        """
        filepath = f"{folder}\\{u_datetime.now(format='NUM')}_{name}.log"
        self._loguru = LoGuru(filepath=filepath)

    def _log(self, **kwargs) -> None:
        """
        ========================================================================
         Description: Log.
        ========================================================================
        """
        """
        if self._verbose:
            values = (str(val) for val in kwargs.values())
            print(self.__deli.join(values))
        """
        if self._loguru:
            adds = kwargs.pop('adds')
            kwargs.update(adds)
            self._loguru.log(kwargs)
