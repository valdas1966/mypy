from f_gui.layout.rect._factory import FactoryRect
from f_gui.layout.bounds.bounds import Bounds


class FactoryBounds:
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
        bounds = FactoryRect.half()
        return Bounds(relative=bounds)

    @staticmethod
    def quarter() -> Bounds:
        """
        ========================================================================
         Generate a quarter position.
        ========================================================================
        """
        bounds = FactoryRect.quarter()
        return Bounds(relative=bounds)
