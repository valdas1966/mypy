from f_gui_old.shapes.i_0_base import Shape
from f_gui_old.mixins.has_position import HasPosition, Position


class Rect(Shape, HasPosition):
    """
    =======================================================================
     Rect-Shape.
    =======================================================================
    """ 

    def __init__(self,
                 name: str = 'Rect',
                 position: Position = Position()) -> None:
        """
        =======================================================================
         Init private attributes.
        =======================================================================
        """
        Shape.__init__(self, name=name)
        HasPosition.__init__(self, position=position)
