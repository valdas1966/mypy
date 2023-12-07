from f_data_structure.graphs.i_0_grid import GraphGrid
from f_heuristic_search.domain.grid.node import Node


class Graph(GraphGrid):
    """
    ============================================================================
     Graph for Grid-Based Heuristic Search.
    ============================================================================
    """

    def __init__(self,
                 rows: int = None,
                 cols: int = None,
                 name: str = None) -> None:
        GraphGrid.__init__(rows=rows, cols=cols, name=name, type_node=Node)
