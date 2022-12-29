from f_abstract.inittable import Inittable


class Loggable(Inittable):

    # Inittable
    def _add_atts(self) -> None:
        """
        ========================================================================
         Description: Add additional attributes to those in the init.
        ========================================================================
        """
        super()._add_atts()
        # bool : Print Logs on Screen
        self._verbose = True
        # str : Delimiter in Print-Logging
        self.__deli = ' | '

    def _log(self, **kwargs) -> None:
        """
        ========================================================================
         Description: Log.
        ========================================================================
        """
        if self._verbose:
            values = (str(val) for val in kwargs.values())
            print(self.__deli.join(values))
