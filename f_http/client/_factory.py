from f_http.client.main import Client
from f_http.response.main import Response


class Factory:
    """
    ============================================================================
     Factory for creating Response instances via Client.
    ============================================================================
    """

    @staticmethod
    def valid() -> Response:
        """
        ========================================================================
         Returns a valid response.
        ========================================================================
        """
        url = "https://jsonplaceholder.typicode.com/posts/1"
        return Client.get_json(url=url)

    @staticmethod
    def invalid() -> Response:
        """
        ========================================================================
         Returns an invalid response (404 - Not Found).
        ========================================================================
        """
        url = "https://jsonplaceholder.typicode.com/posts/999"
        return Client.get_json(url=url)
