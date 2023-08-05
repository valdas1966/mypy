from enum import Enum, auto


class ClockDirection(Enum):
    CLOCKWISE = auto()
    COUNTER_CLOCKWISE = auto()


class DistanceMetric(Enum):
    MANHATTAN = auto()


class CoordinateSystem(Enum):
    CARTESIAN = auto()
