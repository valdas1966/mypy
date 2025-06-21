from f_http.status.inner.f_status import FactoryStatus
from f_http.responses.json import ResponseJson


class FactoryResponseJson:

    @staticmethod
    def ok() -> ResponseJson:
        """
        ========================================================================
         Returns a valid response.
        ========================================================================
        """
        status = FactoryStatus.ok()
        data = {'key': 'value'}
        elapsed = 0.1
        exception = None
        return ResponseJson(status=status,
                            data=data,
                            elapsed=elapsed,
                            exception=exception)
    
    @staticmethod
    def not_found() -> ResponseJson:
        """
        ========================================================================
         Returns a not found response.
        ========================================================================
        """
        status = FactoryStatus.not_found()
        data = None
        elapsed = 0.1
        exception = None
        return ResponseJson(status=status,
                            data=data,
                            elapsed=elapsed,
                            exception=exception)
    
    @staticmethod
    def unknown() -> ResponseJson:
        """
        ========================================================================
         Returns an unknown response.
        ========================================================================
        """
        status = FactoryStatus.unknown()
        data = None
        elapsed = 0.1
        exception = 'Unknown error'
        return ResponseJson(status=status,
                            data=data,
                            elapsed=elapsed,
                            exception=exception)
    
    