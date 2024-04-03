from f_heuristic_search.problem_types.spp.i_0_concrete import SPPConcrete, NodePath
from f_heuristic_search.algos.mixins.has_generated import HasGenerated
from f_heuristic_search.algos.mixins.has_expanded import HasExpanded
from f_data_structure.collections.i_1_queue import QueueBase
from abc import ABC, abstractmethod
from typing import Generic, TypeVar, Type

Node = TypeVar('Node', bound=NodePath)


class SPPAlgoBase(ABC, Generic[Node], HasGenerated[Node], HasExpanded[Node]):
    """
    ============================================================================
     Abstract-Class for a Shortest-Path-Problem Algorithm.
    ============================================================================
    """

    def __init__(self,
                 spp: SPPConcrete,
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

    @property
    # Shortest Path Problem
    def spp(self) -> SPPConcrete:
        return self._spp

    @property
    # True if found a path from Start to Goal
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
            best = self._generated.pop()
            if best == self.spp.goal:
                self._is_path_found = True
                break
            self._expand_node(node=best)

    def optimal_path(self) -> list[Node]:
        """
        ========================================================================
         Returns an Optimal-Path from Start to Goal (empty list if unreachable).
        ========================================================================
        """
        if not self.is_path_found:
            return list()
        return self.spp.goal.path_from_root()

    def _generate_node(self, node: Node, parent: Node = None) -> None:
        """
        ========================================================================
         Generate a Node.
        ========================================================================
        """
        node.update_parent(parent=parent)
        self._generated.push(node)

    def _expand_node(self, node: Node) -> None:
        """
        ========================================================================
         Expand a Node.
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
