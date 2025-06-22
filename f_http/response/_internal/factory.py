from f_http.status._internal.factory import FactoryStatus
from f_http.response.response import Response


class FactoryResponse:
    """
    ========================================================================
     Factory to create the response object.
    ========================================================================
    """

    @staticmethod
    def ok() -> Response:
        """
        ========================================================================
         Returns a valid response.
        ========================================================================
        """
        status = FactoryStatus.ok()
        data = {'key': 'value'}
        elapsed = 0.1
        exception = None
        return Response(status=status,
                        data=data,
                        elapsed=elapsed,
                        exception=exception)
    
    @staticmethod
    def not_found() -> Response:
        """
        ========================================================================
         Returns a not found response.
        ========================================================================
        """
        status = FactoryStatus.not_found()
        data = None
        elapsed = 0.1
        exception = None
        return Response(status=status,
                        data=data,
                        elapsed=elapsed,
                        exception=exception)
    
    @staticmethod
    def unknown() -> Response:
        """
        ========================================================================
         Returns an unknown response.
        ========================================================================
        """
        status = FactoryStatus.none()
        data = None
        elapsed = 0.1
        exception = 'Unknown error'
        return Response(status=status,
                        data=data,
                        elapsed=elapsed,
                        exception=exception)

    
Response.Factory = FactoryResponse
