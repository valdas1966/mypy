from f_core.mixins.has_row_col import HasRowCol


class GenHasRowCol:
    """
    ============================================================================
     Generator for HasRowCol.
    ============================================================================
    """ 

    @staticmethod
    def gen_arg() -> HasRowCol:
        """
        ========================================================================
         Generate an instance of HasRowCol.
        ========================================================================
        """
        return HasRowCol(row=1, col=2)
