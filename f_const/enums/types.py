from enum import Enum


class TypeComparison(Enum):
    """
    ========================================================================
     Type of Comparison.
    ========================================================================
    """
    GREATER = 'GREATER'
    EQUAL = 'EQUAL'
    LESS = 'LESS'
    GREATER_EQUAL = 'GREATER_EQUAL'
    LESS_EQUAL = 'LESS_EQUAL'
    NOT_EQUAL = 'NOT_EQUAL'