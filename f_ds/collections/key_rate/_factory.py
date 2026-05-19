from f_ds.collections.key_rate.main import KeyRate


class Factory:
    """
    ========================================================================
     Factory for the KeyRate class.
    ========================================================================
    """

    @staticmethod
    def a() -> KeyRate:
        """
        ====================================================================
         KeyRate 'a': 3 positive, 1 negative -> rate 0.75.
        ====================================================================
        """
        return KeyRate(item='a', pos=3, neg=1)

    @staticmethod
    def b() -> KeyRate:
        """
        ====================================================================
         KeyRate 'b': 1 positive, 3 negative -> rate 0.25.
        ====================================================================
        """
        return KeyRate(item='b', pos=1, neg=3)

    @staticmethod
    def none_rate() -> KeyRate:
        """
        ====================================================================
         KeyRate 'z': 0 positive, 0 negative -> rate None.
        ====================================================================
        """
        return KeyRate(item='z', pos=0, neg=0)
