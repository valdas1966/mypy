
class MyWorkBookInit:
    """
    ============================================================================
     Desc: Wraps the openpyxl.workbook Class.
    ============================================================================
    """

    def __init__(self, xlsx: str) -> None:
        """
        ========================================================================
         Description: Init Attributes.
        ========================================================================
        """
        assert type(xlsx) == str, type(xlsx)
        # Path to XL-File
        self._xlsx = xlsx
        # Working Excel-WorkBook
        self._wb = None
