from __future__ import annotations
from f_gui.shapes.i_1_rect import Rect, Shape, Position
from f_ds.mixins.has_hierarchy import HasHierarchy


class Container(Rect, HasHierarchy[Shape]):
    """
    =======================================================================
     Container-Shape.   
    =======================================================================
    """

    def __init__(self,
                 name: str = 'Container',
                 position: Position = Position(),
                 parent: Container = None) -> None:
        """
        =======================================================================
         Init private attributes.
        =======================================================================
        """
        Rect.__init__(self, name=name, position=position)
        HasHierarchy.__init__(self, parent=parent)

    def _update_parent(self) -> None:
        """
        =======================================================================
         Update the parent of the container.
        =======================================================================
        """
        self.position.parent = self.parent.position.absolute
