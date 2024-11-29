from typing import Generic, TypeVar
from abc import ABC, abstractmethod
from f_core.mixins.has_rows_cols import HasRowsCols


T = TypeVar('T')


class ContainerBase(Generic[T], HasRowsCols):
    """
    ============================================================================
     Base class for list Container to manage items in list grid layout.
    ============================================================================
    """

    def __init__(self,
                 rows: int = 100,
                 cols: int = 100,
                 name: str = None) -> None:
        """
        ========================================================================
         Initialize the container with the specified number of rows and cols.
        ========================================================================
        """
        HasRowsCols.__init__(self, rows, cols, name)

    @abstractmethod
    def add(self,
            item: T,
            row: int,
            col: int,
            span_rows: int = 1,
            span_cols: int = 1) -> None:
        """
        ========================================================================
         Add an Item at the specified Position with the given Spans.
        ========================================================================
        """
        pass
