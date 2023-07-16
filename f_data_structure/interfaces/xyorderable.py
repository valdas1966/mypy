from f_data_structure.interfaces.xyable import XYAble
from enum import Enum, auto


class CoordinateSystem(Enum):
    CARTESIAN = auto()


class XYOrderable(XYAble):
    """
    ============================================================================
     Desc: Represent a XYAble object that can be ordered
            (Default = Cartesian Coordinate System).
    ============================================================================
     Inherited Properties:
    ----------------------------------------------------------------------------
        1. x (int): Object's X-Coordinate in the 2D-Space.
        2. y (int): Object's Y-Coordinate in the 2D-Space.
    ----------------------------------------------------------------------------
        1. distance(other: 'XYAble') -> int : Return Manhattan-Distance between
                                              this and other XYAble object.
    ============================================================================
     Properties:
    ----------------------------------------------------------------------------
        1. coordinate_system (CoordinateSystem): The ordering system used.
    ============================================================================
    """

    def __init__(self,
                 x: int,
                 y: int,
                 coordinate_system: CoordinateSystem = CoordinateSystem.CARTESIAN):
        super().__init__(x=x, y=y)
        self._coordinate_system = coordinate_system

    @property
    def coordinate_system(self) -> CoordinateSystem:
        return self._coordinate_system

    def __lt__(self, other: 'XYOrderable') -> bool:
        if self.coordinate_system == CoordinateSystem.CARTESIAN:
            return self.y < other.y or (self.y == other.y and self.x < other.x)

    def __le__(self, other: 'XYOrderable') -> bool:
        if self.coordinate_system == CoordinateSystem.CARTESIAN:
            return self < other or self == other

    def __gt__(self, other: 'XYOrderable') -> bool:
        if self.coordinate_system == CoordinateSystem.CARTESIAN:
            return not (self <= other)

    def __ge__(self, other: 'XYOrderable') -> bool:
        if self.coordinate_system == CoordinateSystem.CARTESIAN:
            return not (self < other)
