from typing import Any
from f_core.mixins.validatable.main import Validatable
from f_http.status.main import Status


class Response(Validatable):
    """
    ========================================================================
     Result object returned by:
        Client.get_json(url, params, headers) -> Response
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
                 status: Status | None,
                 # Response's data
                 data: dict[str, Any] | None,
                 # Response's elapsed time (in seconds)
                 elapsed: float | None,
                 # Response's exception message (if failed)
                 exception: str | None = None) -> None:
        """
        ========================================================================
         Initialize the Response object.
        ========================================================================
        """
        self._data = data
        self._elapsed = elapsed
        self._status = status
        self._exception = exception
        is_valid = bool(self._status) and (data is not None)
        Validatable.__init__(self, is_valid=is_valid)

    @property
    def status(self) -> Status | None:
        """
        ========================================================================
         Get the status code of the response.
        ========================================================================
        """
        return self._status

    @property
    def data(self) -> dict[str, Any] | None:
        """
        ========================================================================
         Get the data of the response.
        ========================================================================
        """
        return self._data

    @property
    def elapsed(self) -> float | None:
        """
        ========================================================================
         Get the elapsed time of the response.
        ========================================================================
        """
        return self._elapsed

    @property
    def exception(self) -> str | None:
        """
        ========================================================================
         Get the exception message of the response.
        ========================================================================
        """
        return self._exception

    def __str__(self) -> str:
        """
        ========================================================================
         Return the string representation of the response.
        ========================================================================
        """
        code = self._status.code if self._status else None
        has_data = self._data is not None
        return f'Code={code}, Data={has_data}, Elapsed={self._elapsed}'
