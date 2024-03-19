from __future__ import annotations
from typing import Type
from f_data_structure.graphs.i_0_grid import GraphGrid
from f_heuristic_search.nodes.i_3_f_cell import NodeFCell as Node


class Graph(GraphGrid):
    """
    ============================================================================
     Graph for Grid-Based Heuristic Search.
    ============================================================================
    """

    def __init__(self,
                 rows: int,
                 cols: int = None,
                 name: str = None) -> None:
        """
        ========================================================================
         Inits an empty Graph by its Grid's dimensions (rows and cols).
        ========================================================================
        """
        GraphGrid.__init__(self,
                           rows=rows,
                           cols=cols,
                           name=name,
                           type_node=Node)

    @classmethod
    def generate(cls,
                 rows: int,
                 cols: int = None,
                 pct_non_valid: int = 0,
                 type_node: Type[Node] = Node) -> Graph:
        """
        ========================================================================
         Generate a Graph with random Grid by given:
        ------------------------------------------------------------------------
            1. Dimensions (Rows and Cols).
            2. Percent of Non-Valid Nodes (Obstacles).
            3. Type of Node the Grid will consist.
        ========================================================================
        """
        return GraphGrid.generate(rows=rows,
                                  cols=cols,
                                  pct_non_valid=pct_non_valid,
                                  type_node=type_node)

    @classmethod
    def generate_many(cls,
                      cnt: int,
                      rows: int,
                      cols: int = None,
                      pct_non_valid: int = 0,
                      type_node: Type[Node] = Node) -> list[Graph]:
        """
        ========================================================================
         Generate a list of Graphs with random Grids by given:
        ------------------------------------------------------------------------
            1. Dimensions (Rows and Cols).
            2. Percent of Non-Valid Nodes (Obstacles).
            3. Type of Node the Grid will consist.
        ========================================================================
        """
        res = list()
        for _ in range(cnt):
            g = Graph.generate(rows=rows,
                               cols=cols,
                               pct_non_valid=pct_non_valid,
                               type_node=type_node)
            res.append(g)
        return res
