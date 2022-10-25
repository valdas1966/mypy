from f_utils import u_dict


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
            self.__dict__[key] = val
        self._add_kwargs()

    def _add_kwargs(self) -> None:
        """
        ========================================================================
         Description: Add additional KWARgs. Requires implementation.
        ========================================================================
        """
        pass

    def _filter_kwargs(self, keys: 'sequence') -> dict:
        """
        ========================================================================
         Description: Return kwargs filtered by keys.
        ========================================================================
        """
        return u_dict.filter_by_keys(d=self.__dict__, keys=keys)
