from __future__ import annotations
from f_core.processes.i_2_io import ProcessIO
from abc import abstractmethod
from typing import Generic, TypeVar

Input = TypeVar('Input')
Output = TypeVar('Output')
State = TypeVar('State')
Ops = TypeVar('Ops')


class AlgoGraph(Generic[Input, Output], ProcessIO[Input, Output]):
    """
    ============================================================================
     Abstract-Class for Graph-Algorithms in Computer-Science.
    ============================================================================
    """

    def __init__(self,
                 _input: Input,
                 name: str = 'Graph-Algorithm') -> None:
        """
        ========================================================================
         Init private Attributes.
        ========================================================================
        """
        ProcessIO.__init__(self, _input=_input, name=name)

    @abstractmethod
    def _create_state(self) -> State:
        """
        ========================================================================
         Create a State object of the Graph-Algorithm.
        ========================================================================
        """

    @abstractmethod
    def _create_ops(self) -> Ops:
        """
        ========================================================================
         Create an Ops object of the Graph-Algorithm.
        ========================================================================
        """
