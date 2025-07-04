from f_ds.grids.cell.base.main import CellBase
from f_core.mixins.validatable_public import ValidatablePublic


class CellMap(CellBase, ValidatablePublic):
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
                 is_valid: bool = True,
                 # Cell's Name
                 name: str = 'CellMap'
                 ) -> None:
        """
        ========================================================================
         Init private Attributes.
        ========================================================================
        """
        CellBase.__init__(self, row=row, col=col, name=name)
        ValidatablePublic.__init__(self, is_valid=is_valid)
