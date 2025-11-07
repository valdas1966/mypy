from f_graph.old_path.algos.one_to_one.state import StateOneToOne
from f_graph.old_path.funcs.heuristic import Heuristic


class StateOneToMany(StateOneToOne):
    """
    ============================================================================
     State object for One-To-Many Path-Algorithms.
    ============================================================================
    """

    def update(self, heuristic: Heuristic) -> None:
        """
        ========================================================================
         Update the Heuristic of all Nodes in the Generated Queue.
        ========================================================================
        """
        for node in self.generated:
            node.h = heuristic(node)
        self.generated.update()
