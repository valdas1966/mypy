from enum import Enum


class Side(Enum):
    """
    ============================================================================
     Side — one edge of a rectangle (TOP / RIGHT / BOTTOM / LEFT).
    ============================================================================
     Names a connection edge of a `Bounds`; values are the CSS edge keywords
     (matching Border's side names). Each Side carries its outward `normal`
     (a unit direction pointing away from the rectangle, in screen coordinates
     where y grows downward) and its `opposite`. Used to resolve an Element's
     four connection points (`Bounds.anchor`) and to route `Connector`s.
    ============================================================================
    """
    TOP = 'top'
    RIGHT = 'right'
    BOTTOM = 'bottom'
    LEFT = 'left'

    @property
    def normal(self) -> tuple[int, int]:
        """
        ========================================================================
         Outward unit direction (dx, dy) pointing away from the rectangle.
        ========================================================================
         Screen coordinates (y grows downward): TOP=(0,-1), BOTTOM=(0,1),
         LEFT=(-1,0), RIGHT=(1,0).
        ========================================================================
        """
        return _NORMALS[self]

    @property
    def opposite(self) -> 'Side':
        """
        ========================================================================
         The opposing Side (TOP<->BOTTOM, LEFT<->RIGHT).
        ========================================================================
        """
        return _OPPOSITES[self]


# Outward normals (dx, dy) — y grows downward (screen coordinates).
_NORMALS = {
    Side.TOP: (0, -1),
    Side.RIGHT: (1, 0),
    Side.BOTTOM: (0, 1),
    Side.LEFT: (-1, 0),
}

# Opposing side pairs.
_OPPOSITES = {
    Side.TOP: Side.BOTTOM,
    Side.BOTTOM: Side.TOP,
    Side.LEFT: Side.RIGHT,
    Side.RIGHT: Side.LEFT,
}
