from f_core.mixins.has.name import HasName
from abc import ABC 


class Shape(ABC, HasName):
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
        super().__init__(name)
