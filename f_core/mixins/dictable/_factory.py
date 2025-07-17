from f_core.mixins.dictable.main import Dictable


class Factory:
    """
    ========================================================================
     Factory class for creating Dictable objects.
    ========================================================================
    """

    @staticmethod
    def abc() -> Dictable[str, int]:
        """
        ========================================================================
         Create a Dictable object with a, b, c keys and 1, 2, 3 values.
        ========================================================================
        """
        data = {'a': 1, 'b': 2, 'c': 3}
        return Dictable(data=data)
