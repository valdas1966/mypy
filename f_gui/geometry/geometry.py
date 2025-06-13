from f_core.mixins.printable import Printable
from f_core.mixins.comparable import Comparable
from f_gui.geometry.generators.g_bounds import GenBounds, Bounds
from typing import Union

BoundsLike = Union[tuple[float, float, float, float], Bounds]


class Geometry(Printable, Comparable):
    """
    ============================================================================
     A GUI layout utility that manages both relative (to the parent) and
      absolute bounds of a component.
    ============================================================================
     1. The relative bounds are defined as percentages of the parent.
     2. The absolute bounds are auto-computed based on the parent's bounds.   
     3. When the parent geo changes, the absolute bounds update accordingly.
    ============================================================================
    """

    def __init__(self,
                 bounds_relative: BoundsLike = GenBounds.full(),
                 bounds_parent: BoundsLike = GenBounds.full(),
                 ) -> None:
        """
        ========================================================================
         Init private Attributes.
        ========================================================================
        """
        # Initialize the relative bounds
        self._bounds_relative = self._init_bounds_relative(bounds=bounds_relative)
        # Initialize the parent bounds
        self._bounds_parent = self._init_bounds_parent(bounds=bounds_parent)
        # Initialize the absolute bounds
        self._bounds_absolute = None
        # Update the absolute bounds
        self.update_bounds_absolute()

    @property
    def bounds_relative(self) -> Bounds:
        """
        ========================================================================
         Get the object's relative position (top, left, width, height).
        ========================================================================
        """
        return self._bounds_relative

    @bounds_relative.setter
    def bounds_relative(self, val: BoundsLike) -> None:
        """
        ========================================================================
         Set the relative position (top, left, width, height).
        ========================================================================
        """
        if isinstance(val, Bounds):
            self._bounds_relative = val
        else:
            # If val is a tuple, convert it to a Bounds object
            self._bounds_relative = Bounds(*val)

    @property
    def bounds_absolute(self) -> Bounds:
        """
        ========================================================================
         Get the absolute position (top, left, width, height).
        ========================================================================
        """
        return self._bounds_absolute

    @property
    def bounds_parent(self) -> Bounds:
        """
        ========================================================================
         Get the absolute position of the Parent.
        ========================================================================
        """
        return self._bounds_parent

    @bounds_parent.setter
    def bounds_parent(self, val: Bounds) -> None:
        """
        ========================================================================
         Set the parent's absolute position.
        ========================================================================
        """
        # Update the parent bounds
        self._bounds_parent = val
        # Update the absolute position by parent bounds
        self.update_bounds_absolute()

    def update_bounds_absolute(self) -> None:
        """
        ========================================================================
         Update the absolute position based on the parent's dimensions.
        ========================================================================
        """
        # Set the Top-Absolute-Value as a percentage of the parent's height.
        top = (self._bounds_parent.height * self._bounds_relative.top / 100) + self._bounds_parent.top
        # Set the Left-Absolute-Value as a percentage of the parent's width.
        left = (self._bounds_parent.width * self._bounds_relative.left / 100) + self._bounds_parent.left
        # Set the Width-Absolute-Value as a percentage of the parent's width.
        width = (self._bounds_parent.width * self._bounds_relative.width / 100)
        # Set the Height-Absolute-Value as a percentage of the parent's height.
        height = (self._bounds_parent.height * self._bounds_relative.height / 100)
        # Return the absolute bounds
        self._bounds_absolute = Bounds(top, left, width, height)
    
    def key_comparison(self) -> tuple[float, float, float, float]:
        """
        ========================================================================
         Return the key-comparison of the object.
        ========================================================================
        """
        return self.bounds_absolute.to_tuple()

    def _init_bounds_relative(self, bounds: BoundsLike) -> Bounds:
        """
        ========================================================================
         Inits Relative (Bounds).
        ========================================================================
        """ 
        # If bounds is a tuple, convert it to a Bounds object.
        if isinstance(bounds, tuple):
            return Bounds(*bounds)
        # If bounds is already a Bounds object, return it.
        else:
            return bounds

    def _init_bounds_parent(self, bounds: BoundsLike) -> Bounds:
        """
        ========================================================================
         Inits Parent (Bounds).
        ========================================================================
        """ 
        # If bounds is a tuple, convert it to a Bounds object.
        if isinstance(bounds, tuple):
            return Bounds(*bounds)
        # If bounds is already a Bounds object, return it.
        else:
            return bounds
        
    def __str__(self) -> str:
        """
        ========================================================================
         Ex: '(0.2, 0.3, 0.4, 0.5) * (0, 0, 80, 80) -> (16, 24, 32, 40)'
        ========================================================================
        """
        return (f'{self.bounds_relative} X {self.bounds_parent} -> '
                f'{self.bounds_absolute}')
