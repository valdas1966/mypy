from f_gui.geometry.generators.g_bounds import GenBounds
from f_gui.geometry.position import Position


class GenPosition:
    """
    ========================================================================
     Generator for Position objects.
    ========================================================================
    """

    @staticmethod
    def gen_position_half() -> Position:
        """
        ========================================================================
         Generate a half position.
        ========================================================================
        """
        relative = GenBounds.half()
        return Position(relative=relative)
    
    @staticmethod
    def gen_position_quarter() -> Position:
        """
        ========================================================================
         Generate a quarter position.
        ========================================================================
        """
        position = Position()
        position.relative = GenBounds.half()
        position.parent = GenBounds.half()
        return position
