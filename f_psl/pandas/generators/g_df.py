import pandas as pd


class GenDF:
    """
    ============================================================================
     DataFrame Generator Class.
    ============================================================================
    """

    @staticmethod
    def two_hands() -> pd.DataFrame:
        """
        ========================================================================
         Generate a DataFrame of 'two hands'.
        ========================================================================
        """
        a = [1, 2, 3, 4, 5]
        b = [1, 2, 3, 4, 5]
        data = {'a': a, 'b': b}
        return pd.DataFrame(data)
    
    @staticmethod
    def three_hands() -> pd.DataFrame:
        """
        ========================================================================
         Generate a DataFrame of 'three hands'.
        ========================================================================
        """
        a = [1, 2, 3, 4, 5]
        b = [1, 2, 3, 4, 5]
        c = [1, 2, 3, 4, 5]
        data = {'a': a, 'b': b, 'c': c}
        return pd.DataFrame(data)

    @staticmethod
    def missing_multiples() -> pd.DataFrame:
        """
        ========================================================================
         Generate a DataFrame of missing multiples.
        ========================================================================
        """
        x = [0, 4]
        y = [0, 2]
        val = [1, 2]
        data = {'x': x, 'y': y, 'val': val}
        return pd.DataFrame(data)
