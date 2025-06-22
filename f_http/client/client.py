from f_http.response.response import Response
from f_http.status.status import Status
from pathlib import Path
from typing import Any
import requests


class Client:
    """
    ============================================================================
     ClientHttp class for sending HTTP-GET requests (to get json-dict or file).
    ============================================================================
    """

    # Factory to create Responses
    Factory: type = None

    @staticmethod
    def get_json(# URL to send the GET request to
                 url: str,
                 # Parameters to be sent in the GET request
                 params: dict[str, Any] = None,
                 # Headers to be sent in the GET request
                 headers: dict[str, str] = None) -> Response:
        """
        ========================================================================
         Send an HTTP-GET request and parse the response to Response.
        ========================================================================
        """
        # Init the response variables as None (if request fails)
        status: Status | None = None
        data: dict[str, Any] | None = None        
        elapsed: float | None = None
        exception: str | None = None

        # Try to get the response from the URL and parse to Response
        try:
            response = requests.get(url=url, params=params, headers=headers)
            status = Status(code=response.status_code)
            elapsed = round(response.elapsed.total_seconds(), 2)
            if status:
                data = response.json()
        except Exception as e:
            exception = str(e)

        # Return the parsed Response as Response
        return Response(status=status,
                        data=data,
                        elapsed=elapsed,
                        exception=exception)
