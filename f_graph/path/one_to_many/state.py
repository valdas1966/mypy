from f_graph.path.one_to_one.state import StateOneToOne, Queue, Node
from f_graph.path.one_to_one.heuristics import Heuristic
from typing import Type


class StateOneToMany(StateOneToOne):
    """
    ============================================================================
     State object for One-To-Many Path-Algorithms.
    ============================================================================
    """
    def __init__(self, type_queue: Type[Queue]) -> None:
        """
        ========================================================================
         Init private Attributes.
        ========================================================================
        """
        StateOneToOne.__init__(self, type_queue=type_queue)
        self.generated: type_queue[Node] = type_queue()
        self.explored: set[Node] = set()
        self.best: Node | None = None

    def update(self, heuristic: Heuristic) -> None:
        """
        ========================================================================
         Update the Heuristic of all Nodes in the Generated Queue.
        ========================================================================
        """
        for node in self.generated:
            node.h = heuristic(node)
        self.generated.update()