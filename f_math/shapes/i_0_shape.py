from f_core.mixins.has.name import HasName
from f_core.mixins.equatable import Equatable


class Shape(HasName, Equatable):
    """
    =================================================================
     Abstract i_0_element class for all shapes.
    =================================================================
    """

    def __init__(self, name: str = 'Shape'):
        """
        =============================================================
         Initialize the shape.
        =============================================================
        """
        HasName.__init__(self, name)

    @property
    def key(self) -> str:
        """
        =============================================================
         Identify the shape by its name (sub-classes may override).
        =============================================================
        """
        return self.name
