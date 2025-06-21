from f_http.status.status import StatusHttp


class FactoryStatus:

    @staticmethod
    def ok() -> StatusHttp:
        """
        ========================================================================
         Returns a valid status.
        ========================================================================
        """
        return StatusHttp(code=200)
    
    @staticmethod
    def not_found() -> StatusHttp:
        """
        ========================================================================
         Returns a not found status.
        ========================================================================
        """
        return StatusHttp(code=404)
    
    @staticmethod
    def bad_request() -> StatusHttp:
        """
        ========================================================================
         Returns a bad request status.
        ========================================================================
        """
        return StatusHttp(code=400)
    
    @staticmethod               
    def none() -> StatusHttp:
        """
        ========================================================================
         Returns a none status.
        ========================================================================
        """
        return StatusHttp(code=None)
