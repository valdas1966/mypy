from f_core.mixins.validatable.main import Validatable
from f_core.mixins.has.name import HasName
from http import HTTPStatus


class Status(HasName, Validatable):
    """
    ============================================================================
     Thin wrapper for HTTPStatus with validation and readable name.
    ============================================================================
    """

    Factory: type = None

    def __init__(self, code: int | None) -> None:
        """
        ========================================================================
         Initialize private attributes.
        ========================================================================
        """
        self._code = code
        # Try to get the status from the code
        try:
            self._status = HTTPStatus(self._code)
        except ValueError:
            self._status = None
        # Set Status Validity (True if code is 2xx)
        is_valid = code is not None and 200 <= code < 300
        Validatable.__init__(self, is_valid=is_valid)
        # Set Status Name (If status is not found, set to 'UNKNOWN')
        name = self._status.name if self._status else 'UNKNOWN'
        HasName.__init__(self, name=name)

    @property
    def code(self) -> int | None:
        """
        ========================================================================
         Get the code of the status.
        ========================================================================
        """
        return self._code

    def __str__(self) -> str:
        """
        ========================================================================
         Return the string representation of the status.
        ========================================================================
        """
        return f'Code={self.code}, Name={self.name}'
