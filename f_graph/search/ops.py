from f_graph.search.protocols.data import ProtocolData
from f_graph.search.problem import Problem
from f_graph.nodes.i_1_path import NodePath
from typing import Generic, TypeVar

Node = TypeVar('Node', bound=NodePath)


class Ops(Generic[Node]):

    def __init__(self,
                 problem: Problem,
                 data: ProtocolData) -> None:
        self._problem = problem
        self._data = data

    def generate(self, node: Node, parent: Node = None) -> None:
        node.parent = parent
        self._data.mark_generated(node=node)

    def explore(self, node: Node) -> None:
        children = self._problem.graph.neighbors(node)
        for child in children:
            self._process_child(child=child, parent=node)
        self._data.mark_explored(node=node)

    def _process_child(self, child: Node, parent: Node) -> None:
        if self._data.is_explored(node=child):
            return
        if self._data.is_generated(node=child):
            return
        self.generate(node=child, parent=parent)