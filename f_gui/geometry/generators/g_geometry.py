from f_gui.geometry.generators.g_bounds import GenBounds
from f_gui.geometry.geometry import Geometry


class GenGeometry:
    """
    ========================================================================
     Generator for Geometry objects.
    ========================================================================
    """

    @staticmethod
    def gen_geometry_half() -> Geometry:
        """
        ========================================================================
         Generate a half position.
        ========================================================================
        """
        relative = GenBounds.half()
        return Geometry(relative=relative)
    
    @staticmethod
    def gen_geometry_quarter() -> Geometry:
        """
        ========================================================================
         Generate a quarter position.
        ========================================================================
        """
        geometry = Geometry()
        geometry.relative = GenBounds.half()
        geometry.parent = GenBounds.half()
        return geometry
