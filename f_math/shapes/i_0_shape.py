from f_core.mixins.has.name import HasName


class Shape(HasName):
    """
    =================================================================
     Abstract i_0_base class for all shapes.
    =================================================================
    """

    def __init__(self, name: str = 'Shape'):
        """
        =============================================================
         Initialize the shape.
        =============================================================
        """
        HasName.__init__(self, name)

    def key(self) -> str:
        """
        =============================================================
         Return the name of the shape.
        =============================================================
        """
        return HasName.key(self)
