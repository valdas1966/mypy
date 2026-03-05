from .main import HasRowsCols


class Factory:

    @staticmethod
    def gen(rows: int, cols: int | None = None) -> HasRowsCols:
        """
        ========================================================================
         Return a HasRowsCols object with given rows and cols.
        ========================================================================
        """
        return HasRowsCols(rows=rows, cols=cols)

    @staticmethod
    def square_3() -> HasRowsCols:
        """
        ========================================================================
         Return a HasRowsCols object with rows=3 and cols=3.
        ========================================================================
        """
        return HasRowsCols(rows=3)

    @staticmethod
    def rect_5_10() -> HasRowsCols:
        """
        ========================================================================
         Return a HasRowsCols object with rows=5 and cols=10.
        ========================================================================
        """
        return HasRowsCols(rows=5, cols=10)
