from f_ds.geometry.bounds.main import Bounds


class Factory:
    """
    ========================================================================
     Generator for Bounds objects.
    ========================================================================
    """

    @staticmethod
    def full() -> Bounds[float]:
        """
        ========================================================================
         1. Generate a full bounds object.
         2. Assume that the bounds are in the range of 0 to 100.
        ========================================================================
        """
        return Bounds(top=0, left=0, bottom=100, right=100)

    @staticmethod
    def half() -> Bounds[float]:
        """
        ========================================================================
         Generate a centered half-size bounds object (25, 25, 75, 75).
        ========================================================================
        """
        return Bounds(top=25, left=25, bottom=75, right=75)

    @staticmethod
    def quarter() -> Bounds[float]:
        """
        ========================================================================
         Generate a centered quarter-size bounds object
          (37.5, 37.5, 62.5, 62.5).
        ========================================================================
        """
        return Bounds(top=37.5, left=37.5, bottom=62.5, right=62.5)
