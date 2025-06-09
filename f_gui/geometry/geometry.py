from f_core.mixins.printable import Printable
from f_core.mixins.comparable import Comparable
from f_gui.geometry.generators.g_bounds import GenBounds, Bounds
from typing import Union

BoundsLike = Union[tuple[float, float, float, float], Bounds]


class Geometry(Printable, Comparable):
    """
    ============================================================================
     A GUI layout utility that manages both relative and absolute bounds
       of a component.
    ============================================================================
     1. The relative bounds are defined as percentages of the parent.
     2. The absolute bounds are auto-computed based on the parent's bounds.   
     3. When the parent geo changes, the absolute bounds update accordingly.
    ============================================================================
    """

    def __init__(self,
                 relative: BoundsLike = GenBounds.full(),
                 parent: BoundsLike = GenBounds.full(),
                 ) -> None:
        """
        ========================================================================
         Init private Attributes.
        ========================================================================
        """
        # Initialize the relative bounds
        self._relative: Bounds = self._init_relative(relative=relative)
        # Initialize the parent bounds
        self._parent: Bounds = self._init_parent(parent=parent)
        # Initialize the absolute bounds
        self._absolute: Bounds = None
        # Update the absolute bounds
        self.update_absolute()

    @property
    def relative(self) -> Bounds:
        """
        ========================================================================
         Get the object's relative position (top, left, width, height).
        ========================================================================
        """
        return self._relative

    @relative.setter
    def relative(self, val: BoundsLike) -> None:
        """
        ========================================================================
         Set the relative position (left, top, width, height).
        ========================================================================
        """
        if isinstance(val, Bounds):
            self._relative = val
        else:
            self._relative = Bounds(*val)

    @property
    def absolute(self) -> Bounds:
        """
        ========================================================================
         Get the absolute position (left, top, width, height).
        ========================================================================
        """
        return self._absolute

    @property
    def parent(self) -> Bounds:
        """
        ========================================================================
         Get the absolute position of the Parent.
        ========================================================================
        """
        return self._parent

    @parent.setter
    def parent(self, val: Bounds) -> None:
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
        top = (self._parent.height * self._relative.top / 100) + self._parent.top
        # Set the Left-Absolute-Value as a percentage of the parent's width.
        left = (self._parent.width * self._relative.left / 100) + self._parent.left
        # Set the Width-Absolute-Value as a percentage of the parent's width.
        width = (self._parent.width * self._relative.width / 100)
        # Set the Height-Absolute-Value as a percentage of the parent's height.
        height = (self._parent.height * self._relative.height / 100)
        # Return the absolute bounds
        self._absolute = Bounds(top, left, width, height)
    
    def key_comparison(self) -> tuple[float, float, float, float]:
        """
        ========================================================================
         Return the key-comparison of the object.
        ========================================================================
        """
        return self.absolute.to_tuple()

    def _init_relative(self, relative: BoundsLike) -> Bounds:
        """
        ========================================================================
         Inits Relative (Bounds).
        ========================================================================
        """ 
        # If relative is a tuple, convert it to a Bounds object.
        if isinstance(relative, tuple):
            return Bounds(*relative)
        # If relative is already a Bounds object, return it.
        else:
            return relative

    def _init_parent(self, parent: BoundsLike) -> Bounds:
        """
        ========================================================================
         Inits Parent (Bounds).
        ========================================================================
        """ 
        # If parent is a tuple, convert it to a Bounds object.
        if isinstance(parent, tuple):
            parent = Bounds(*parent)
        # Return the parent bounds
        return parent
        
    def __str__(self) -> str:
        """
        ========================================================================
         Ex: '(0.2, 0.3, 0.4, 0.5) * (0, 0, 80, 80) -> (16, 24, 32, 40)'
        ========================================================================
        """
        return f'{self.relative} X {self.parent} -> {self.absolute}'
