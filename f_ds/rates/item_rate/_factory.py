from f_ds.rates.item_rate.main import ItemRate


class Factory:
    """
    ========================================================================
     Factory for the ItemRate class.
    ========================================================================
    """

    @staticmethod
    def a() -> ItemRate:
        """
        ====================================================================
         ItemRate 'a': 3 positive, 1 negative -> rate 0.75.
        ====================================================================
        """
        return ItemRate(item='a', pos=3, neg=1)

    @staticmethod
    def b() -> ItemRate:
        """
        ====================================================================
         ItemRate 'b': 1 positive, 3 negative -> rate 0.25.
        ====================================================================
        """
        return ItemRate(item='b', pos=1, neg=3)

    @staticmethod
    def none_rate() -> ItemRate:
        """
        ====================================================================
         ItemRate 'z': 0 positive, 0 negative -> rate None.
        ====================================================================
        """
        return ItemRate(item='z', pos=0, neg=0)
