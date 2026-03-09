from f_http.response.main import Response
from f_http.status.main import Status
from f_log import get_log, ColorLog as cl
from typing import Any
import requests

_log = get_log(__name__)


class Client:
    """
    ============================================================================
     Client class for sending HTTP-GET requests (to get json-dict).
    ============================================================================
    """

    # Factory to create Responses
    Factory: type = None

    @staticmethod
    def get_json(# URL to send the GET request to
                 url: str,
                 # Parameters to be sent in the GET request
                 params: dict[str, Any] | None = None,
                 # Headers to be sent in the GET request
                 headers: dict[str, str] | None = None,
                 # Timeout in seconds (None = no timeout)
                 timeout: float | None = 30) -> Response:
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
        # Try to get the response from the URL
        try:
            response = requests.get(url=url,
                                    params=params,
                                    headers=headers,
                                    timeout=timeout)
            status = Status(code=response.status_code)
            elapsed = round(response.elapsed.total_seconds(), 2)
        except Exception as e:
            exception = str(e)
        # Try to parse JSON (separately to preserve status/elapsed)
        if status and exception is None:
            try:
                data = response.json()
            except Exception as e:
                exception = str(e)
        # Log the result
        if exception:
            _log.info(f'{cl.label("GET")} {cl.path(url)} '
                      f'{cl.warn(exception)}')
        else:
            code = status.code if status else None
            color = cl.value if status else cl.warn
            _log.info(f'{cl.label("GET")} {cl.path(url)} '
                      f'{color(code)} {cl.time(f"{elapsed}s")}')
        # Return the parsed Response
        return Response(status=status,
                        data=data,
                        elapsed=elapsed,
                        exception=exception)
