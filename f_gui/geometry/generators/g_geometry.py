from f_gui.geometry.generators.g_bounds import GenBounds
from f_gui.geometry.geometry import Geometry


class GenGeometry:
    """
    ========================================================================
     Generator for Geometry objects.
    ========================================================================
    """

    @staticmethod
    def full() -> Geometry:
        return Geometry()


    @staticmethod
    def half() -> Geometry:
        """
        ========================================================================
         Generate a half position.
        ========================================================================
        """
        bounds = GenBounds.half()
        return Geometry(bounds_relative=bounds)

    @staticmethod
    def quarter() -> Geometry:
        """
        ========================================================================
         Generate a quarter position.
        ========================================================================
        """
        bounds = GenBounds.quarter()
        return Geometry(bounds_relative=bounds)
        
