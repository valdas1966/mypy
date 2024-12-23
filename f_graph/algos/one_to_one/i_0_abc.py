from f_graph.algos.i_0_abc import AlgoPath, Queue, Node
from f_graph.problems.i_2_one_to_one import ProblemOneToOne
from f_graph.path.single.ops import OpsNodeOneToOne
from f_graph.path.single.state import DataOneToOne
from abc import abstractmethod
from typing import TypeVar, Type

Problem = TypeVar('Problem', bound=ProblemOneToOne)
OpsNode = TypeVar('OpsNode', bound=OpsNodeOneToOne)
Data = TypeVar('Data', bound=DataOneToOne)


class AlgoOneToOneABC(AlgoPath[Problem, OpsNode, Data, Node]):
    """
    ============================================================================
     ABC for One-to-One Path Algorithm.
    ============================================================================
    """

    def __init__(self,
                 problem: Problem,
                 type_queue: Type[Queue],
                 name: str = None) -> None:
        """
        ========================================================================
         Init private Attributes.
        ========================================================================
        """
        self._path: list[Node] = list()
        AlgoPath.__init__(self,
                          problem=problem,
                          type_queue=type_queue,
                          type_data=DataOneToOne,
                          type_ops_node=OpsNodeOneToOne,
                          name=name)

    def get_path(self) -> list[Node]:
        return self._path

    @abstractmethod
    def _can_terminate(self, best: Node) -> bool:
        pass

    @abstractmethod
    def _construct_path(self, best: Node) -> bool:
        pass

    def _search(self) -> None:
        """
        ========================================================================
         Search the shortest paths from Start to Goal.
        ========================================================================
        """
        self._ops_node.gen(node=self._problem.start)
        while self._data.generated:
            best = self._data.generated.pop()
            if self._can_terminate(best=best):
                self._is_valid = True
                self._construct_path(best=best)
                break
            self._ops_node.explore(node=best)
