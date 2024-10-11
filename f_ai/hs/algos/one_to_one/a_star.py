from f_graph.algos.one_to_one.i_0_base import AlgoOneToOne, ProblemOneToOne
from f_ds.queues.i_1_priority import QueuePriority
from f_ai.hs.nodes.i_1_f import NodeF
from typing import TypeVar, Callable

Problem = TypeVar('Problem', bound=ProblemOneToOne)
Node = TypeVar('Node', bound=NodeF)


class AStar(AlgoOneToOne[Problem, Node]):
    """
    ============================================================================
     A* Algorithm.
    ============================================================================
    """

    def __init__(self,
                 problem: Problem,
                 heuristics: Callable[[Node], int]) -> None:
        """
        ========================================================================
         Init private Attributes.
        ========================================================================
        """
        self._heuristics = heuristics
        AlgoOneToOne.__init__(self, problem=problem, type_queue=QueuePriority)

    def _generate_node(self,
                       node: Node,
                       parent: Node = None) -> None:
        """
        ========================================================================
         Generate a Node (set parent, heuristics and add to generated list).
        ========================================================================
        """
        node.h = self._heuristics(node)
        AlgoOneToOne._generate_node(self, node=node, parent=parent)

    def _try_update_node(self,
                         node: Node,
                         parent: Node) -> None:
        """
        ========================================================================
         Try update a generated Node with new Parent.
        ========================================================================
        """
        if node.is_better_parent(parent_new=parent):
            node.parent = parent
