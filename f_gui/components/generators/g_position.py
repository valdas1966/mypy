from f_gui.components.generators.g_ltwh import GenLTWH
from f_gui.components.position import Position


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
        relative = GenLTWH.gen_ltwh_half()
        return Position(relative=relative)
    
    @staticmethod
    def gen_position_quarter() -> Position:
        """
        ========================================================================
         Generate a quarter position.
        ========================================================================
        """
        position = Position()
        position.relative = GenLTWH.gen_ltwh_quarter()
        position.parent = GenLTWH.gen_ltwh_half()
        return position


pos = GenPosition.gen_position_half()
print(pos)
