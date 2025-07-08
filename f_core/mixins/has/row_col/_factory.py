from f_core.mixins.has.row_col.main import HasRowCol


def create_has_row_col(row: int = None, col: int = None) -> HasRowCol:
    """
    ============================================================================
     Factory function to create HasRowCol instances.
    ============================================================================
    """
    return HasRowCol(row, col)