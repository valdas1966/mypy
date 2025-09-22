from f_hs.ds.nodes.i_1_cost.main import NodeCost
from f_ds.grids import CellMap as Cell


class Factory:
    """
    ============================================================================
     Factory for creating nodes with cost values.
    ============================================================================
    """
    
    @staticmethod
    def cell_00() -> NodeCost[Cell]:
        """
        ========================================================================
         Create a new node with the cell (0, 0).
        ========================================================================
        """
        cell = Cell(0, 0)   
        node = NodeCost(key=cell, h=5)
        return node
    
    @staticmethod
    def cell_01() -> NodeCost[Cell]:
        """
        ========================================================================
         Create a new node with the cell (0, 1).
        ========================================================================
        """
        cell = Cell(0, 1)   
        node = NodeCost(key=cell, h=4)
        return node

    @staticmethod
    def cell_11() -> NodeCost[Cell]:
        """
        ========================================================================
         Create a new node with the cell (1, 1).
        ========================================================================
        """
        cell = Cell(1, 1)
        node = NodeCost(key=cell, h=3)
        return node
   