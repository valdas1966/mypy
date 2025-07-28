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
         Return a HasRowCol object with row and col set to 1 and 2.
        ========================================================================
        """
        return HasRowCol(row=1)

    @staticmethod
    def twelve() -> HasRowCol:
        """
        ========================================================================
         Return a HasRowCol object with row and col set to 12.
        ========================================================================
        """
        return HasRowCol(row=1, col=2)
