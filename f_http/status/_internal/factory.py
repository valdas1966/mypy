from f_http.status.status import Status


class FactoryStatus:

    @staticmethod
    def ok() -> Status:
        """
        ========================================================================
         Returns a valid status.
        ========================================================================
        """
        return Status(code=200)
    
    @staticmethod
    def not_found() -> Status:
        """
        ========================================================================
         Returns a not found status.
        ========================================================================
        """
        return Status(code=404)
    
    @staticmethod
    def bad_request() -> Status:
        """
        ========================================================================
         Returns a bad request status.
        ========================================================================
        """
        return Status(code=400)
    
    @staticmethod               
    def none() -> Status:
        """
        ========================================================================
         Returns a none status.
        ========================================================================
        """
        return Status(code=None)
