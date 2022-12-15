from f_abstract.inittable import Inittable


class MyWorkSheetBase(Inittable):
    """
    ============================================================================
     Description: Excel-WorkSheet Init by openpyxl.worksheet
    ============================================================================
    """

    # openpyxl.worksheet : The working WorkSheet
    ._ws = None
