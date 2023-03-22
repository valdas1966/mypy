from f_utils import u_file


class MyWorkBookInit:
    """
    ============================================================================
     Desc: Wraps the openpyxl.workbook Class.
    ============================================================================
    """

    def __init__(self, xlsx: str = None) -> None:
        """
        ========================================================================
         Description: Init Attributes.
        ========================================================================
        """
        # Path to XL-File
        self._xlsx = xlsx
        # Working Excel-WorkBook
        self._wb = None
