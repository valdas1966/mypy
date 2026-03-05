from .main import HasRowCol


class Factory:
    
    @staticmethod
    def zero() -> HasRowCol:
        """
        ========================================================================
         Return a HasRowCol object with row and col set to 0.
        ========================================================================
        """
        return HasRowCol()

    @staticmethod
    def one() -> HasRowCol:
        """
        ========================================================================
         Return a HasRowCol object with row and col set to 1.
        ========================================================================
        """
        return HasRowCol(row=1)

    @staticmethod
    def twelve() -> HasRowCol:
        """
        ========================================================================
         Return a HasRowCol object with row set to 1 and col set to 2.
        ========================================================================
        """
        return HasRowCol(row=1, col=2)
