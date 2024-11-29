from f_core.inittable import Inittable
from f_logging.c_loguru import LoGuru
from f_logging.c_stack_driver import StackDriver
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
        # StackDriver
        if not hasattr(self, '_stack_driver'):
            self._stack_driver = None
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

    def _create_stack_driver(self, json_key: str, name: str) -> None:
        self._stack_driver = StackDriver(json_key=json_key, name=name)

    def _log(self, **kwargs) -> None:
        """
        ========================================================================
         Description: Log.
        ========================================================================
        """
        if self._verbose:
            values = (str(val) for val in kwargs.values() if val is not None)
            print(self.__deli.join(values))
        adds = kwargs.pop('adds')
        kwargs.update(adds)
        kwargs = {k: v for k, v in kwargs.items() if
                  k not in ('bq', 'wa', 'stack_driver')}
        kwargs = {k: v for k, v in kwargs.items() if v is not None}
        if self._stack_driver:
            self._stack_driver.log(struct=kwargs)
        if self._loguru:
            self._loguru.log(kwargs)
