from typing import Any
from f_core.mixins.validatable.main import Validatable
from f_http.status.status import Status


class Response(Validatable):
    """
    ========================================================================
     Result object returned by:
        ClientHttp.json(url, params, headers) -> Response
    ------------------------------------------------------------------------
     Properties:
    ------------------------------------------------------------------------
       1. data: dict[str, Any]
       2. status: Status
       3. elapsed: float (time in seconds)
       4. exception: str (error message if request fails)
    ========================================================================
    """

    # Factory to create the response object
    Factory: type = None

    def __init__(self,
                 # Response's status
                 status: Status,
                 # Response's data
                 data: dict[str, Any],
                 # Response's elapsed time (in seconds)
                 elapsed: float,
                 # Response's exception message (if failed)
                 exception: str = None) -> None:
        """
        ========================================================================
         Initialize the ResponseAPI object.
        ========================================================================
        """
        self._data = data
        self._elapsed = elapsed
        self._status = status
        self._exception = exception
        is_valid = bool(self._status) and (data is not None)
        Validatable.__init__(self, is_valid=is_valid)

    @property
    def status(self) -> Status:
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
    def exception(self) -> str:
        """
        ========================================================================
         Get the exception message of the response.
        ========================================================================
        """
        return self._exception
