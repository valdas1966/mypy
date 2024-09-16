from f_http.get import HttpGet
from abc import ABC


class RequestBase(ABC):
    """
    ============================================================================
     Base-Class for Rapid-API Requests.
    ============================================================================
    """

    def __init__(self,
                 key: str,
                 host: str,
                 headers: dict[str, str]) -> None:
        """
        ========================================================================
         Init private Attributes.
        ========================================================================
        """
        self._key = key
        self._host = host
        self._headers = headers

    def request(self,
                url: str,
                params: dict[str, str]) -> HttpGet:
        """
        ========================================================================
         Return Request-Result.
        ========================================================================
        """
        response = HttpGet(url, params, self._headers)
        if response.status == 403:
            print('HTTP 403 Forbidden')
        return response
