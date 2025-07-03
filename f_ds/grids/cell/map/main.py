from f_core.mixins.has_row_col import HasRowCol
from f_core.mixins.validatable_public import ValidatablePublic


class CellMap(HasRowCol, ValidatablePublic):
    """
    ============================================================================
     Cell-Map for the 2D-Grid Maps.
    ============================================================================
    """ 
    
    # Factory
    Factory: type = None
    
    def __init__(self,
                 # Cell's Row
                 row: int,
                 # Cell's Column
                 col: int,
                 # Cells's Validity
                 is_valid: bool = True
                 ) -> None:
        """
        ========================================================================
         Init private Attributes.
        ========================================================================
        """
        HasRowCol.__init__(self, row=row, col=col)
        ValidatablePublic.__init__(self, is_valid=is_valid)
        