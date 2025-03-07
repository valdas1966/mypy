from f_core.mixins.printable import Printable
from f_core.mixins.has_name import HasName


class Shape(HasName, Printable):
    """
    =======================================================================
     Abstract base class for all GUI-Shapes.
    =======================================================================
    """
    
    def __init__(self, name: str = 'Shape') -> None:
        """
        =======================================================================
         Init private attributes.
        =======================================================================    
        """
        HasName.__init__(self, name=name)
        Printable.__init__(self)

    def __str__(self) -> str:
        """
        =======================================================================
         Return the string representation of the shape.
        =======================================================================    
        """
        return f'{self.name}'
    