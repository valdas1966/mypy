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
    def two_hands_reversed() -> pd.DataFrame:
        """
        ========================================================================
         Generate a DataFrame of 'two hands' reversed.
        ========================================================================
        """
        a = [1, 2, 3, 4, 5] 
        b = [5, 4, 3, 2, 1]
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

    @staticmethod
    def wide_to_long() -> pd.DataFrame:
        """
        ========================================================================
         Generate a DataFrame of wide to long.
        ========================================================================
        """
        x = [1, 2]
        y_1 = [10, 20]
        y_2 = [30, 40]
        y_3 = [50, 60]
        data = {'x': x, 'y_1': y_1, 'y_2': y_2, 'y_3': y_3}
        return pd.DataFrame(data)
    
    @staticmethod
    def group_by_col() -> pd.DataFrame:
        """
        ========================================================================
         Generate a DataFrame of group by col.
        ========================================================================    
        """
        a = [1, 1, 2, 2]
        b = [1, 2, 3, 4]
        data = {'a': a, 'b': b}
        return pd.DataFrame(data)

