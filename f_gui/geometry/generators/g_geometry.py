from f_gui.geometry.generators.g_bounds import GenBounds
from f_gui.geometry.geometry import Geometry


class GenGeometry:
    """
    ========================================================================
     Generator for Geometry objects.
    ========================================================================
    """

    @staticmethod
    def half() -> Geometry:
        """
        ========================================================================
         Generate a half position.
        ========================================================================
        """
        relative = GenBounds.half()
        return Geometry(bounds_relative=relative)

    @staticmethod
    def quarter() -> Geometry:
        """
        ========================================================================
         Generate a quarter position.
        ========================================================================
        """
        relative = GenBounds.quarter()
        return Geometry(bounds_relative=relative)
        
