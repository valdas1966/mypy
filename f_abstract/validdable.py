from f_abstract.inittable import Inittable


class Validdable(Inittable):
    """
    ============================================================================
     Description: Class with Validity-Indication and Error-MSG.
    ============================================================================
    """

    # Inittable
    def _add_atts(self) -> None:
        """
        ========================================================================
         Description: Add additional attributes to those in the init.
        ========================================================================
        """
        super()._add_atts()
        # bool : Object-Validity
        self._is_valid = None
        # str : Error-Message
        self._e_msg = None

    @property
    def is_valid(self) -> bool:
        return self._is_valid

    @property
    def e_msg(self) -> str:
        return self._e_msg
