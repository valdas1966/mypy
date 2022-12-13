from f_abstract.inittable import Inittable


class Validdable(Inittable):
    """
    ============================================================================
     Description: Class with Validity-Indication and Error-MSG.
    ============================================================================
    """

    # bool : Object-Validity
    _is_valid = None

    # str : Error-Message
    _e_msg = None

    @property
    def is_valid(self) -> bool:
        return self._is_valid

    @property
    def e_msg(self) -> str:
        return self._e_msg
