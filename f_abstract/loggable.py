from f_abstract.inittable import Inittable


class Loggable(Inittable):

    # bool : Print Logs
    _verbose = True

    # str : Delimiter in Print-Logging
    __deli = ' | '

    def _pre_log(self, **kwargs) -> None:
        self._log(**kwargs)

    def _post_log(self, **kwargs) -> None:
        self._log(**kwargs)

    def _log(self, **kwargs) -> None:
        """
        ========================================================================
         Description: Log.
        ========================================================================
        """
        if self._verbose:
            values = (str(val) for val in kwargs.values())
            print(self.__deli.join(values))
