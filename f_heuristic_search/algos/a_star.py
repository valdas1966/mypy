from f_heuristic_search.algos.mixins.has_open_closed import HasOpenClosed
from f_heuristic_search.algos.mixins.sppable import SPPAble
from f_heuristic_search.problem_types.spp import SPP
from f_data_structure.nodes.node_3_f import NodeF as Node
from f_data_structure.open import Open
from f_data_structure.closed import Closed
from f_data_structure.f_grid.cell import Cell


class AStar(SPPAble, HasOpenClosed):
    """
    ============================================================================
     A* Algorithm.
    ============================================================================
     Methods:
    ----------------------------------------------------------------------------
        1. run() -> None
           [*] Executes the Algorithm.
    ============================================================================
     Inherited Methods:
    ----------------------------------------------------------------------------
        1. optimal_path() -> list[NodeCell]
           [*] Returns an Optimal-Path from Start to Node.
               An empty list is returned if the Goal is unreachable.
    ============================================================================
    """

    # SPPAble
    spp: SPP                      # Shortest Path Problem
    is_path_found: bool           # True if found a path from Start to Goal
    # HasOpenClose
    open: Open                    # Queue of generated nodes (not expanded yet)
    closed: Closed                # Set of expanded nodes in insertion order

    def __init__(self, spp: SPP) -> None:
        SPPAble.__init__(self, spp)
        HasOpenClosed.__init__(self)

    def run(self) -> None:
        """
        ========================================================================
         Executes the Algorithm.
        ========================================================================
        """
        self.open.push(self.spp.start)
        while len(self.open):
            best = self.open.pop()
            self.closed.push(best)
            if best == self.spp.goal:
                self._is_path_found = True
                return
            self._expand_node(best)
        # Path not found
        self._is_path_found = False

    def _expand_node(self, node: Node) -> None:
        """
        ========================================================================
         Visits the Node and Generates its Children.
        ========================================================================
        """
        for child in self._get_children(node):
            if self._is_expanded(child):
                continue
            if self._is_generated(child):
                self._try_new_parent(child=child, parent=node)
            else:
                self._generate_node(child)

    def _generate_node(self, cell: Cell) -> None:
        """
        ========================================================================
         Generates a Node from a Cell and inserts it into an Open list.
        ========================================================================
        """
        node = Node.from_cell(cell)
        node.h = node.distance(self.spp.goal)
        self.open.push(node)

    def _get_children(self, node: Node) -> list[Cell]:
        """
        ========================================================================
         Returns a List of Node's Children.
        ========================================================================
        """
        return [cell
                for cell
                in self.spp.grid.neighbors(node)
                if not cell == node.parent]

    def _is_expanded(self, cell: Cell) -> bool:
        """
        ========================================================================
         Returns True if the given Cell is have already been expanded.
        ========================================================================
        """
        return cell in self.closed

    def _is_generated(self, cell: Cell) -> bool:
        """
        ========================================================================
         Returns True if the given Cell is have already generated.
        ========================================================================
        """
        return cell in self.open

    def _try_new_parent(self, child: Node, parent: Node) -> None:
        node = self.open.get(child)
        if node.is_better_parent(parent):
            node.parent = parent
