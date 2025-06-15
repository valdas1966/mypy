from f_gui.layout.generators.g_rect import GenRect
from f_gui.layout.bounds import Bounds


class GenBounds:
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
        bounds = GenRect.half()
        return Bounds(relative=bounds)

    @staticmethod
    def quarter() -> Bounds:
        """
        ========================================================================
         Generate a quarter position.
        ========================================================================
        """
        bounds = GenRect.quarter()
        return Bounds(relative=bounds)
