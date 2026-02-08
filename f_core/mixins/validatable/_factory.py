from f_core.mixins.validatable.main import Validatable


class Factory:
    """
    ========================================================================
     Factory for the Validatable class.
    ========================================================================
    """

    @staticmethod
    def valid() -> Validatable:
        """
        ========================================================================
         Create a Validatable object.
        ========================================================================
        """
        return Validatable(is_valid=True)

    @staticmethod
    def invalid() -> Validatable:
        """
        ========================================================================
         Create a Validatable object.
        ========================================================================
        """
        return Validatable(is_valid=False)
