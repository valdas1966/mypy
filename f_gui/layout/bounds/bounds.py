from f_core.mixins.printable import Printable
from f_core.mixins.comparable import Comparable
from f_gui.layout.rect._factory import FactoryRect
from f_gui.layout.rect.rect import Rect
from typing import Union

RectLike = Union[tuple[float, float, float, float], Rect]


class Bounds(Printable, Comparable):
    """
    ============================================================================
     A GUI layout utility that manages both relative (to the parent) and
      absolute bounds of a component.
    ============================================================================
     1. The relative bounds are defined as percentages of the parent.
     2. The absolute bounds are auto-computed based on the parent's bounds.   
     3. When the parent's bounds changes, the absolute bounds update auto.
    ============================================================================
    """

    # Factory
    Factory: type = None

    def __init__(self,
                 # Object's Relative bounds (default is full)
                 relative: RectLike = FactoryRect.full(),
                 # Object's Parent bounds (default is full)
                 parent: RectLike = FactoryRect.full(),
                 ) -> None:
        """
        ========================================================================
         Init private Attributes.
        ========================================================================
        """
        # Initialize the object's relative bounds
        self._relative = self._init_relative(bounds=relative)
        # Initialize the object's parent absolute bounds
        self._parent = self._init_parent(bounds=parent)
        # Initialize the object's absolute bounds
        self._absolute = None
        # Update the object's absolute bounds
        self.update_absolute()

    @property
    def relative(self) -> Rect:
        """
        ========================================================================
         Get the object's relative position (top, left, width, height).
        ========================================================================
        """
        return self._relative

    @relative.setter
    def relative(self, val: RectLike) -> None:
        """
        ========================================================================
         Set the relative position (top, left, width, height).
        ========================================================================
        """
        if isinstance(val, Rect):
            self._relative = val
        else:
            # If val is a tuple, convert it to a Rect object
            self._relative = Rect(*val)

    @property
    def absolute(self) -> Rect:
        """
        ========================================================================
         Get the absolute position (top, left, width, height).
        ========================================================================
        """
        return self._absolute

    @property
    def parent(self) -> Rect:
        """
        ========================================================================
         Get the absolute position of the Parent.
        ========================================================================
        """
        return self._parent

    @parent.setter
    def parent(self, val: Rect) -> None:
        """
        ========================================================================
         Set the parent's absolute position.
        ========================================================================
        """
        # Update the parent bounds
        self._parent = val
        # Update the absolute position by parent bounds
        self.update_absolute()

    def update_absolute(self) -> None:
        """
        ========================================================================
         Update the absolute position based on the parent's dimensions.
        ========================================================================
        """
        # Set the Top-Absolute-Value as a percentage of the parent's height.
        offset_top = (self._parent.height * self._relative.top / 100)
        top = offset_top + self._parent.top
        # Set the Left-Absolute-Value as a percentage of the parent's width.
        offset_left = (self._parent.width * self._relative.left / 100)
        left = offset_left + self._parent.left
        # Set the Width-Absolute-Value as a percentage of the parent's width.
        width = (self._parent.width * self._relative.width / 100)
        # Set the Height-Absolute-Value as a percentage of the parent's height.
        height = (self._parent.height * self._relative.height / 100)
        # Return the absolute bounds
        self._absolute = Rect(top, left, width, height)
    
    def key_comparison(self) -> tuple[float, float, float, float]:
        """
        ========================================================================
         Return the key-comparison of the object.
        ========================================================================
        """
        # Compare by the object's absolute bounds (as tuple)
        return self.absolute.to_tuple()

    def _init_relative(self, bounds: RectLike) -> Rect:
        """
        ========================================================================
         Inits Relative (Rect).
        ========================================================================
        """ 
        # If bounds is a tuple, convert it to a Rect object.
        if isinstance(bounds, tuple):
            return Rect(*bounds)
        # If bounds is already a Rect object, return it.
        else:
            return bounds

    def _init_parent(self, bounds: RectLike) -> Rect:
        """
        ========================================================================
         Inits Parent (Rect).
        ========================================================================
        """ 
        # If bounds is a tuple, convert it to a Rect object.
        if isinstance(bounds, tuple):
            return Rect(*bounds)
        # If bounds is already a Rect object, return it.
        else:
            return bounds
        
    def __str__(self) -> str:
        """
        ========================================================================
         Ex: '(0.2, 0.3, 0.4, 0.5) * (0, 0, 80, 80) -> (16, 24, 32, 40)'
        ========================================================================
        """
        # Return the object's relative, parent and absolute bounds
        return (f'{self.relative} X {self.parent} -> '
                f'{self.absolute}')
