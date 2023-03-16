
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
        assert isinstance(xlsx, str) or xlsx is None, type(xlsx)
        # Path to XL-File
        self._xlsx = xlsx
        # Working Excel-WorkBook
        self._wb = None
