from f_heuristic_search.nodes.i_3_f_cell import NodeFCell as Node


class HasStart:
    """
    ============================================================================
     Mixin-Class for Problems with a Start Node.
    ============================================================================
    """

    def __init__(self, start: Node) -> None:
        self._start = start

    @property
    def start(self) -> Node:
        return self._start
