from f_core.mixins.has_name import HasName
from abc import ABC 


class Shape(ABC, HasName):
    """
    =================================================================
     Abstract base class for all shapes.
    =================================================================
    """

    def __init__(self, name: str = 'Shape'):
        """
        =============================================================
         Initialize the shape.
        =============================================================
        """
        super().__init__(name)
