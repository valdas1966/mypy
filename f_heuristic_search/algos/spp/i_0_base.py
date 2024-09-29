from f_heuristic_search.problem_types.spp.i_0_concrete import SPPConcrete, NodePath
from f_heuristic_search.algos.mixins.has_generated import HasGenerated
from f_heuristic_search.algos.mixins.has_expanded import HasExpanded
from f_data_structure.collections.i_1_queue import QueueBase
from abc import ABC, abstractmethod
from typing import Generic, TypeVar, Type

SPP = TypeVar('SPP', bound=SPPConcrete)
Node = TypeVar('Node', bound=NodePath)


class AlgoSPPBase(ABC,
                  Generic[SPP, Node],
                  HasGenerated[Node],
                  HasExpanded[Node]):
    """
    ============================================================================
     1. Abstract-Class for list Shortest-Path-Problem Algorithm.
     2. The SPP-Algo should have Generated and Expanded lists (Open & Closed).
    ============================================================================
    """

    def __init__(self,
                 spp: SPP,
                 type_queue: Type[QueueBase]) -> None:
        """
        ========================================================================
         Init private attributes.
        ========================================================================
        """
        HasGenerated.__init__(self, type_queue=type_queue)
        HasExpanded.__init__(self)
        self._spp = spp
        self._is_path_found = None
        self._best: Node = None

    @property
    # Shortest Path Problem
    def spp(self) -> SPP:
        return self._spp

    @property
    # True if found list paths from Start to Goal
    def is_path_found(self) -> bool:
        return self._is_path_found

    def run(self) -> None:
        """
        ========================================================================
         Run the Algorithm.
        ========================================================================
        """
        self._generate_node(node=self.spp.start)
        while self._generated:
            self._best = self._generated.pop()
            if self._can_terminate():
                self._is_path_found = True
                break
            self._expand_node(node=self._best)

    def path_optimal(self) -> list[Node]:
        """
        ========================================================================
         Returns an Optimal-Path from Start to Goal (empty list if unreachable).
        ========================================================================
        """
        if not self.is_path_found:
            return list()
        return self.spp.goal.path_from_root()

    def _can_terminate(self) -> bool:
        """
        ========================================================================
         Return True if the Goal is the Best-Node in Generated-List.
        ========================================================================
        """
        return self._best == self.spp.goal

    def _generate_node(self, node: Node, parent: Node = None) -> None:
        """
        ========================================================================
         Generate list Node.
        ========================================================================
        """
        node.update_parent(parent=parent)
        self._generated.push(node)

    def _expand_node(self, node: Node) -> None:
        """
        ========================================================================
         Expand list Node.
        ========================================================================
        """
        for child in self.spp.graph.get_neighbors(node=node):
            if child not in self.expanded:
                self._process_child(child=child, parent=node)
        self._expanded.add(node)

    @abstractmethod
    def _process_child(self, child: Node, parent: Node) -> None:
        """
        ========================================================================
         Process the Child of the expanded Node.
        ========================================================================
        """
        pass
