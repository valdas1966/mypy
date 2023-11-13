from f_heuristic_search.problem_types.spp import SPP
from f_heuristic_search.nodes.i_2_f_cell import NodeFCell as Node
from f_data_structure.f_grid.grid_cells import GridCells as Grid


class SPPGrid(SPP):
    """
    ============================================================================
     Represents a Shortest-Path-Problem Type in 2D-Grids.
    ============================================================================
    """

    def __init__(self,
                 grid: Grid,
                 start: Node,
                 goal: Node) -> None:
        SPP.__init__(self, start, goal)
        self._grid = grid

    def generate_node(self, node: Node) -> None:
        """
        ========================================================================
         Set Heuristic (Manhattan) Distance to Goal-Node.
        ========================================================================
        """
        node.h = node.distance(self.goal)

    def get_children(self, node: Node) -> list[Node]:
        """
        ========================================================================
         Return Node's Children after converting them into Nodes.
        ========================================================================
        """
        return [Node(parent=node, cell=cell)
                for cell
                in self._grid.neighbors(node)
                if cell != node.parent]

    def __str__(self) -> str:
        res = f'SPP[{self.grid.name}]: '
        res += f'{self.start} -> {self.goal}'
        return res

    def __repr__(self) -> str:
        return str(self)

    @classmethod
    def generate(cls,
                 rows: int,
                 cols: int = None,
                 name: str = None,
                 pct_non_valid: int = 0
                 ) -> SPP:
        """
        ========================================================================
         Generates a random SPP based on the given arguments, which include the
          grid size, as well as random locations for the start, goal, and
          invalid nodes.
        ========================================================================
        """
        grid = Grid.generate(rows=rows,
                             cols=cols,
                             name=name,
                             pct_non_valid=pct_non_valid)
        # Ensure the Grid can accommodate both Start and Goal Cells
        if len(grid.cells()) < 2:
            return None
        start, goal = grid.cells_random(size=2)
        return SPPGrid(grid, start, goal)
