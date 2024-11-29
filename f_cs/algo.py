from __future__ import annotations
from f_core.processes.i_2_io import ProcessIO
from abc import abstractmethod
from typing import Generic, TypeVar

Input = TypeVar('Input')
Output = TypeVar('Output')
Data = TypeVar('Data')
Ops = TypeVar('Ops')


class Algo(Generic[Input, Output], ProcessIO[Input, Output]):
    """
    ============================================================================
     Abstract-Class for Algorithms in Computer-Science.
    ============================================================================
    """

    def __init__(self,
                 _input: Input,
                 name: str = 'Algorithm') -> None:
        """
        ========================================================================
         Init private Attributes.
        ========================================================================
        """
        ProcessIO.__init__(self, _input=_input, name=name)

    @abstractmethod
    def _create_data(self) -> Data:
        """
        ========================================================================
         Create a Data object.
        ========================================================================
        """

    @abstractmethod
    def _create_ops(self) -> Ops:
        """
        ========================================================================
         Create an Ops object.
        ========================================================================
        """
