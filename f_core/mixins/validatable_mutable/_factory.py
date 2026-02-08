from f_core.mixins.validatable_mutable.main import ValidatableMutable


class Factory:
    """
    ========================================================================
     Factory for the ValidatableMutable class.
    ========================================================================
    """

    @staticmethod
    def valid() -> ValidatableMutable:
        """
        ========================================================================    
         Create a ValidatableMutable object.
        ========================================================================
        """
        return ValidatableMutable(is_valid=True)

    @staticmethod
    def invalid() -> ValidatableMutable:
        """
        ========================================================================
         Create a ValidatableMutable object.
        ========================================================================
        """
        return ValidatableMutable(is_valid=False)
