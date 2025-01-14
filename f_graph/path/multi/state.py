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
        self._generated: Counter[Node] = Counter()
        self._explored: Counter[Node] = Counter()

    def update(self, state: StateSingle) -> None:
        """
        ========================================================================
         Update the State from StateSingle.
        ========================================================================
        """
        self._generated.update(state.generated)
        self._explored.update(state.explored)
