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
