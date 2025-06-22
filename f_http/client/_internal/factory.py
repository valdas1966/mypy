from f_http.client.client import Client, Response


class FactoryClientHttp:
    """
    ========================================================================
     Factory to create valid and invalid Response using ClientHttp.
    ========================================================================
    """

    @staticmethod
    def valid() -> Response:
        """
        ========================================================================
         Returns a valid response.   
        ========================================================================
        """
        url_valid = "https://jsonplaceholder.typicode.com/posts/1"
        return Client.get_json(url=url_valid)

    @staticmethod
    def invalid() -> Response:
        """
        ========================================================================
         Returns an invalid response (404 - Not Found).
        ========================================================================
        """ 
        url_invalid = "https://jsonplaceholder.typicode.com/posts/999"
        return Client.get_json(url=url_invalid)
