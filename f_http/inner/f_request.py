from f_http.client import ClientHttp, ResponseAPI


class FactoryRequest:
    """
    ========================================================================
     Class for generating valid and invalid responses.
    ========================================================================
    """

    @staticmethod
    def valid() -> ResponseAPI:
        """
        ========================================================================
         Returns a valid response.   
        ========================================================================
        """
        url_valid = "https://jsonplaceholder.typicode.com/posts/1"
        return ClientHttp.get(url=url_valid)
    
    @staticmethod
    def invalid() -> ResponseAPI:
        """
        ========================================================================
         Returns an invalid response (404 - Not Found).
        ========================================================================
        """ 
        url_invalid = "https://jsonplaceholder.typicode.com/posts/999"
        return ClientHttp.get(url=url_invalid)
