from f_ds.mixins.indexable.main import Indexable


class Factory:

    @staticmethod
    def abc() -> Indexable[str]:
        """
        ========================================================================
         Create an Indexable object with the 'a', 'b', 'c' items.
        ========================================================================
        """
        class ABC(Indexable[str]):
            def to_iterable(self) -> list[str]:
                return list('abc')
        return ABC()
