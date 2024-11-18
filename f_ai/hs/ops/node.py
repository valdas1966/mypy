from f_graph.path_finding.components.ops import OpsNodeABC, Problem, DataOneToOne
from f_ai.hs.nodes.i_1_f import NodeF
from typing import TypeVar, Callable

Node = TypeVar('Node', bound=NodeF)


class OpsNodeHS(OpsNodeABC[Problem, Node]):
    """
    ============================================================================
     Class for Node's Operations in PathFinding-Heuristic-Algorithms.
    ============================================================================
    """

    def __init__(self,
                 problem: Problem,
                 data: DataOneToOne,
                 heuristics: Callable[[Node], int]) -> None:
        """
        ========================================================================
         Init private Attributes.
        ========================================================================
        """
        OpsNodeABC.__init__(self, problem=problem, data=data)
        self._heuristics = heuristics

    def generate(self,
                 node: Node,
                 parent: Node = None) -> None:
        """
        ========================================================================
         Set Node's Heuristics (heuristic distance to Goal) before generating.
        ========================================================================
        """
        node.h = self._heuristics(node)
        OpsNodeABC.generate(self, node=node, parent=parent)

    def try_update(self,
                   child: Node,
                   parent: Node) -> None:
        """
        ========================================================================
         Update child's parent if the new has a better F-Value.
        ========================================================================
        """
        if child.is_better_parent(parent_new=parent):
            child.parent = parent
