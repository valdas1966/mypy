from f_core.mixins.printable import Printable
from f_core.processes.i_2_io import ProcessIO
from f_http.get.config import Input, Output, Reasons
from requests import request, exceptions, Response


class RequestGet(ProcessIO[Input, Output], Printable):
    """
    ============================================================================
     Http Request Get.
    ============================================================================
    """

    def __init__(self,
                 _input: Input,
                 name: str = None) -> None:
        """
        ========================================================================
         Init private Attributes.
        ========================================================================
        """
        ProcessIO.__init__(self, _input=_input, name=name)
        self._reason: Reasons | None = None

    @property
    def reason(self) -> Reasons:
        """
        ========================================================================
         Return the Reason for Fail.
        ========================================================================
        """
        return self._reason

    def run(self) -> Output:
        """
        ========================================================================
         Run the Http Get-Request process.
        ========================================================================
        """
        self._run_pre()
        response = self._request()
        self._run_post()
        return Output(response=response, reason=self.reason)

    def _request(self) -> Response:
        """
        ========================================================================
         Execute the Http Get-Request and return the Response.
        ========================================================================
        """
        response = None
        self._is_valid = False
        try:
            response = request(method='GET',
                               url=self._input.url,
                               params=self._input.params,
                               headers=self._input.headers)
            if response.ok:
                self._is_valid = True
            else:
                self._set_reason(status_code=response.status_code)
        except exceptions.ConnectionError:
            self._reason = Reasons.COMMUNICATION
        except exceptions.Timeout:
            self._reason = Reasons.TIMEOUT
        except exceptions.RequestException:
            self._reason = Reasons.UNKNOWN
        return response

    def _set_reason(self, status_code: int) -> None:
        """
        ========================================================================
         Set the Reason for Fail by the Status-Code.
        ========================================================================
        """
        if status_code == 403:
            self._reason = Reasons.FORBIDDEN
        elif status_code == 401:
            self._reason = Reasons.UNAUTHORIZED
        elif status_code == 404:
            self._reason = Reasons.NOT_FOUND
        elif status_code == 500:
            self._reason = Reasons.SERVER_ERROR
        elif status_code == 400:
            self._reason = Reasons.BAD_REQUEST
        elif status_code == 429:
            self._reason = Reasons.RATE_LIMIT

    def __str__(self) -> str:
        """
        ========================================================================
         Ex: {'music_id': '123', 'count': '20', 'cursor': '20'} ->
             is_valid=True, elapsed=1.08
        ========================================================================
        """
        return (f'{self._input.params} -> is_valid={bool(self)},'
                f' elapsed={self.elapsed()}')
