from .main import NodeCell, Cell


class Factory:
    """
    ============================================================================
     Factory for NodeCell.
    ============================================================================
    """
    
    @staticmethod
    def twelve() -> NodeCell:
        """
        ========================================================================
         Create a NodeCell with a Cell.
        ========================================================================
        """
        cell = Cell.Factory.twelve()
        return NodeCell(cell=cell)
