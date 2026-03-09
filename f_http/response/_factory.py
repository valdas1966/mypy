from f_http.status import Status
from f_http.response.main import Response


class Factory:
    """
    ============================================================================
     Factory for creating Response instances.
    ============================================================================
    """

    @staticmethod
    def ok() -> Response:
        """
        ========================================================================
         Returns a valid response (200 OK with data).
        ========================================================================
        """
        status = Status.Factory.ok()
        return Response(status=status,
                        data={'key': 'value'},
                        elapsed=0.1)

    @staticmethod
    def not_found() -> Response:
        """
        ========================================================================
         Returns a not found response (404).
        ========================================================================
        """
        status = Status.Factory.not_found()
        return Response(status=status,
                        data=None,
                        elapsed=0.1)

    @staticmethod
    def unknown() -> Response:
        """
        ========================================================================
         Returns an unknown response (no status, with exception).
        ========================================================================
        """
        status = Status.Factory.unknown()
        return Response(status=status,
                        data=None,
                        elapsed=0.1,
                        exception='Unknown error')
