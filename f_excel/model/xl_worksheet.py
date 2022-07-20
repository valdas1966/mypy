from f_logging.dec import log_all_methods, log_info_class


#@log_all_methods(decorator=log_info_class)
class MyExcelWorkSheet:

    def __init__(self,
                 wb: 'MyExcelWorkBook',
                 ws: 'MyExcelWorkSheet'):
        """
        ========================================================================
         Description: Constructor. Open Excel-WorkBook with specified WorkSheet
                       by its Title or Index. Default - Open the first Sheet.
        ========================================================================
        """
        # Working Excel-WorkBook
        self._wb = wb
        # Set the Working Excel-WorkSheet
        self._ws = ws

    def set_title(self, title: str) -> None:
        """
        ========================================================================
         Description: Set a Title for the Working Excel-WorkSheet.
        ========================================================================
        """
        try:
            self._ws.title = title
        except Exception as e:
            self._wb.close()
            raise Exception(e)
