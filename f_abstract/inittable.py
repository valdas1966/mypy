from f_utils import u_class


class Inittable:

    def __init__(self, **kwargs):
        """
        ========================================================================
         Description: Constructor.
        ------------------------------------------------------------------------
            1. Set initial KWArgs.
            2. Set additional manual KWArgs (requires func implementation).
        ========================================================================
        """
        for key, val in kwargs.items():
            if not key[0] == '_':
                key = f'_{key}'
            self.__dict__[key] = val
        self._init_add_atts()
        self._init_run_funcs()

    def _init_add_atts(self) -> None:
        """
        ========================================================================
         Description: Add additional attributes to those in the __init__.
        ========================================================================
        """
        pass

    def _init_run_funcs(self) -> None:
        """
        ==============================================================================
         Desc: Run functions in the Init process.
        ==============================================================================
        """
        pass

    def _get_protected_atts(self) -> dict:
        """
        ========================================================================
         Desc: Return a dict of Protected-Attributes (include the Inherited).
        ========================================================================
        """
        d = u_class.get_protected_atts(self=self)
        return {key[1:]: val for key, val in d.items()}
