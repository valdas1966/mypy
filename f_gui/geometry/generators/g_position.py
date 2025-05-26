from f_gui.geometry.generators.g_tlwh import GenTLWH
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
        relative = GenTLWH.half()
        return Position(relative=relative)
    
    @staticmethod
    def gen_position_quarter() -> Position:
        """
        ========================================================================
         Generate a quarter position.
        ========================================================================
        """
        position = Position()
        position.relative = GenTLWH.half()
        position.parent = GenTLWH.half()
        return position


pos = GenPosition.gen_position_quarter()
print(pos)