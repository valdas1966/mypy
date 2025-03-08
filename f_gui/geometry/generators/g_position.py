from f_gui.geometry.generators.g_tlwh import GenLTWH
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
        relative = GenLTWH.half()
        return Position(relative=relative)
    
    @staticmethod
    def gen_position_quarter() -> Position:
        """
        ========================================================================
         Generate a quarter position.
        ========================================================================
        """
        position = Position()
        position.relative = GenLTWH.half()
        position.parent = GenLTWH.half()
        return position
