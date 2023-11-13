from f_data_structure.f_tree.node import Node


class SPP:
    """
    ============================================================================
     Represents a Shortest-Path-Problem in Heuristic Search.
    ============================================================================
    """

    def __init__(self,
                 start: Node,
                 goal: Node,
                 nodes: list[Node] = None,
                 edges: dict[Node, list[Node]] = None) -> None:
        start.name = 'START'
        goal.name = 'GOAL'
        self._start = start
        self._goal = goal
        self._nodes = nodes
        self._edges = edges

    @property
    # SPP Start-Node
    def start(self) -> Node:
        return self._start

    @property
    # SPP Goal-Node
    def goal(self) -> Node:
        return self._goal

    @property
    # All SPP Nodes
    def nodes(self) -> set[Node]:
        return self._nodes

    def get_children(self, node: Node) -> list[Node]:
        """
        ========================================================================
         Return List of Node's Children.
        ========================================================================
        """
        return [child for child in self._edges[node] if child != node.parent]
