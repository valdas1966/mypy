from typing import Any
from f_core.mixins.validatable import Validatable
from f_http.inner.status.status import StatusHttp


class ResponseJson(Validatable):
    """
    ========================================================================
     Result object returned by:
        ClientHttp.json(url, params, headers) -> ResponseJson
    ------------------------------------------------------------------------
     Properties:
    ------------------------------------------------------------------------
    |   1. data: dict[str, Any]
    |   2. status: int (200 ok, 404 not found, other - errors)
    |   3. elapsed: float (time in seconds)
    |   4. is_found: bool (True if status is 200, False otherwise)
    |   5. reason: str (explanation of why the request failed)
    ========================================================================
    """

    def __init__(self,
                 data: dict[str, Any],
                 status: int,
                 elapsed: float) -> None:
        """
        ========================================================================
         Initialize the ResponseAPI object.
        ========================================================================
        """
        self._data = data       
        self._elapsed = elapsed
        self._status = StatusHttp(code=status)
        is_valid = bool(self._status) and (data is not None)
        Validatable.__init__(self, is_valid=is_valid)

    @property
    def status(self) -> StatusHttp:
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
    
