from f_core.mixins.has.rows_cols.main import HasRowsCols


def create_has_rows_cols(rows: int, cols: int = None) -> HasRowsCols:
    """
    ============================================================================
     Factory function to create HasRowsCols instances.
    ============================================================================
    """
    return HasRowsCols(rows, cols)