from f_gui.layout.bounds.main import Bounds
from f_math.shapes.rect import Rect


class Factory:
    """
    ========================================================================
     Generator for Bounds objects.
    ========================================================================
    """

    @staticmethod
    def full() -> Bounds:
        return Bounds()

    @staticmethod
    def half() -> Bounds:
        """
        ========================================================================
         Generate a half position.
        ========================================================================
        """
        bounds = Rect.Factory.half()
        return Bounds(relative=bounds)

    @staticmethod
    def quarter() -> Bounds:
        """
        ========================================================================
         Generate a quarter position.
        ========================================================================
        """
        bounds = Rect.Factory.quarter()
        return Bounds(relative=bounds)
