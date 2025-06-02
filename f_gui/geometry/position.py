from f_core.mixins.printable import Printable
from f_core.mixins.comparable import Comparable
from f_gui.geometry.generators.g_bounds import GenBounds, Bounds
from typing import Union

BoundsLike = Union[tuple[float, float, float, float], Bounds]


class Position(Printable, Comparable):
    """
    ============================================================================
     1. Component-Class to manage relative and absolute positions.
     2. Position inits with a relative position (optionally with a parent).
     3. The absolute position is updated automatically on parent-change.
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
        self._parent: Bounds     = self._init_parent(parent=parent)
        # Initialize the absolute bounds
        self._absolute: Bounds = self._update_absolute()

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
        self._absolute = self._update_absolute()

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
    
    def _update_absolute(self) -> Bounds:
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
        return Bounds(top, left, width, height)
        
    def __str__(self) -> str:
        """
        ========================================================================
         Ex: '(0.2, 0.3, 0.4, 0.5) * (0, 0, 80, 80) -> (16, 24, 32, 40)'
        ========================================================================
        """
        return f'{self.relative} X {self.parent} -> {self.absolute}'


pos = Position(relative=GenBounds.half())
print(pos)
parent = GenBounds.half()
pos.parent = parent
print(pos)

