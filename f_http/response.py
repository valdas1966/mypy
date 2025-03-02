from f_core.mixins.validatable import Validatable

class ResponseAPI(Validatable):
    """
    ========================================================================
     Custom response object to store API request results.
    ========================================================================
    """

    def __init__(self,
                 data: dict,
                 status: int,
                 elapsed: float) -> None:
        """
        ========================================================================
         Initialize the ResponseAPI object.
        ========================================================================
        """
        self._data = data
        self._status = status       
        self._elapsed = elapsed
        is_valid = False
        if self.status:
            if 200 <= self.status < 400:
                if data is not None:
                    is_valid = True
            if self.status == 404:
                is_valid = True
        Validatable.__init__(self, is_valid=is_valid)

    @property
    def status(self) -> int:
        """
        ========================================================================
         Get the status code of the response.
        ========================================================================
        """ 
        return self._status    

    @property
    def data(self) -> dict:
        """
        ========================================================================
         Get the data of the response.
        ========================================================================
        """
        return self._data

    @property
    def elapsed(self) -> float:
        """
        ========================================================================
         Get the elapsed time of the response.
        ========================================================================
        """
        return self._elapsed
    
    @property
    def is_found(self) -> bool:
        """
        ========================================================================
         Check if the requested item is found.
        ========================================================================
        """
        return self.status == 200
    
    def reason(self) -> str:
        """
        ========================================================================
         Returns a human-readable explanation of why the request failed.
        ========================================================================
        """
        if self.data is None:
            return "Cannot convert JSON to dict."
        if not self.status:
            return "No status code returned."  
        if self.status == 200:
            return "OK: The request was successful."
        if self.status == 400:
            return "Bad Request: The request was invalid or cannot be processed."
        if self.status == 401:
            return "Unauthorized: Authentication is required or failed."
        if self.status == 403:
            return "Forbidden: Access to this resource is denied."
        if self.status == 404:
            return "Not Found: The requested resource does not exist."
        if self.status == 408:
            return "Request Timeout: The server took too long to respond."
        if self.status == 429:
            return "Too Many Requests: The API rate limit has been exceeded."
        if 500 <= self.status < 600:
            return f"Server Error ({self.status}): The server encountered an error."
        return f"Request failed with status code {self.status}."
