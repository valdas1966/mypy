from f_graph.path.state import StatePath, Node
from f_graph.path.single.state import StateSingle
from collections import Counter


class StateMulti(StatePath):
    """
    ============================================================================
     State of Multiple-Goal Path-Algorithms.
    ============================================================================
    """

    def __init__(self) -> None:
        """
        ========================================================================
         Init private Attributes.
        ========================================================================
        """
        StatePath.__init__(self)
        self.generated: Counter[Node] = Counter()
        self.explored: Counter[Node] = Counter()

    def update(self, state: StateSingle) -> None:
        """
        ========================================================================
         Update the State from StateSingle.
        ========================================================================
        """
        self.generated.update(state.generated)
        self.explored.update(state.explored)
