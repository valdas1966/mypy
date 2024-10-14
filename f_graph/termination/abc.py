from f_graph.problems.i_0_graph import ProblemGraph
from abc import ABC, abstractmethod
from typing import TypeVar

Problem = TypeVar('Problem', bound=ProblemGraph)


class TerminationABC(ABC):

    @abstractmethod
    def can(self, *args) -> bool:
        pass
