from f_ds.pair.main import Pair


class Factory:

    @staticmethod
    def ab_ordered() -> Pair[str]:
        """
        ========================================================================
         Return a Pair with the 'a' and 'b' items.
        ========================================================================
        """
        return Pair(a='a', b='b', is_ordered=True)

    @staticmethod
    def ab_unordered() -> Pair[str]:
        """
        ========================================================================
         Return a Pair with the 'a' and 'b' items.
        ========================================================================
        """
        return Pair(a='a', b='b', is_ordered=False)

    @staticmethod
    def ba_ordered() -> Pair[str]:
        """
        ========================================================================
         Return a Pair with the 'b' and 'a' items.
        ========================================================================
        """
        return Pair(a='b', b='a', is_ordered=True)

    @staticmethod
    def ba_unordered() -> Pair[str]:
        """
        ========================================================================
         Return a Pair with the 'b' and 'a' items.
        ========================================================================
        """
        return Pair(a='b', b='a', is_ordered=False)     
