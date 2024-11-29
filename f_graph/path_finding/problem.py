from __future__ import annotations
from f_core.mixins.nameable import Nameable
from f_core.abstracts.copyable import Copyable
from f_graph.graphs.i_1_grid import GraphGrid
from f_graph.nodes.i_1_path_cell import NodePathCell
from collections.abc import Collection
from typing import Generic, TypeVar

Graph = TypeVar('Graph', bound=GraphGrid)
Node = TypeVar('Node', bound=NodePathCell)


class Problem(Generic[Graph, Node], Nameable, Copyable):
    """
    ============================================================================
     Graph-Path Problem.
    ============================================================================
    """

    def __init__(self,
                 graph: Graph,
                 start: Node,
                 goals: Collection[Node],
                 name: str = 'Path-Problem') -> None:
        """
        ========================================================================
         Init private Attributes.
        ========================================================================
        """
        Nameable.__init__(self, name=name)
        self._graph = graph
        self._start = start
        self._goals = set(goals)

    @property
    def graph(self) -> Graph:
        """
        ========================================================================
         Return the Graph of the Problem.
        ========================================================================
        """
        return self._graph

    @property
    def start(self) -> Node:
        """
        ========================================================================
         Return the Start Node of the Problem.
        ========================================================================
        """
        return self._start

    @property
    def goals(self) -> set[Node]:
        """
        ========================================================================
         Return the Goals Nodes of the Problem.
        ========================================================================
        """
        return self._goals.copy()

    def get_children(self, node: Node) -> list[Node]:
        """
        ========================================================================
         Return List of Node's Children.
        ========================================================================
        """
        return self._graph.children(node=node)

    def copy(self) -> Problem:
        """
        ========================================================================
         Return a Copy of the Problem.
        ========================================================================
        """
        graph = self._graph.copy()
        start = graph[self._start.cell.row, self._start.cell.col]
        goals = {graph[goal.cell.row, goal.cell.col] for goal in self._goals}
        return Problem(graph=graph, start=start, goals=goals, name=self._name)

    def __str__(self) -> str:
        """
        ========================================================================
         Return STR-REPR of the Problem.
        ========================================================================
         Ex: Path-Problem([0,0] -> [1,1])
        ========================================================================
        """
        return f'{Nameable.__str__(self)}({self._start} -> {self._goals})'
