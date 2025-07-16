from .main import Collectionable


class Factory:
    """
    ============================================================================
     Factory for creating Collectionable objects.
    ============================================================================
    """

    @staticmethod
    def abc() -> Collectionable[str]:
        """
        ========================================================================
         Create a Collectionable object with the 'a', 'b', 'c' items.
        ========================================================================
        """
        class ABC(Collectionable[str]):
            def to_iterable(self) -> list[str]:
                return list('abc')
            
        return ABC()
