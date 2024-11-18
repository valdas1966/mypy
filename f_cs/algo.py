from __future__ import annotations
from f_abstract.processes.i_2_io import ProcessIO
from typing import Generic, TypeVar

Input = TypeVar('Input')
Output = TypeVar('Output')
Data = TypeVar('Data')
Ops = TypeVar('Ops')


class Algo(Generic[Input, Output, Data, Ops],
           ProcessIO[Input, Output]):
    """
    ============================================================================
     Abstract-Class for Algorithms in Computer-Science.
    ============================================================================
    """

    def __init__(self,
                 _input: Input,
                 data: Data,
                 ops: Ops,
                 name: str = 'Algorithm') -> None:
        """
        ========================================================================
         Init private Attributes.
        ========================================================================
        """
        ProcessIO.__init__(self, _input=_input, name=name)
        self._data = data
        self._ops = ops
