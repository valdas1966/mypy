from f_abstract.mixins.printable import Printable
from f_abstract.mixins.validatable import Validatable
from requests import request, Response
import json
import time


class Get(Printable, Validatable):
    """
    ============================================================================
     Http Request Get.
    ============================================================================
    """

    def __init__(self,
                 url: str,
                 params: dict = None,
                 headers: dict = None) -> None:
        """
        ========================================================================
         Init private Attributes.
        ========================================================================
        """
        Validatable.__init__(self, is_valid=False)
        self._url: str = url
        self._params: dict[str, str] = params or dict()
        self._headers: dict[str, str] = headers or dict()
        self._response: Response | None = None
        self._elapsed: float | None = None
        self._request()
        if self._response is not None and self._response.status_code == 200:
           self.set_valid()
        else:
            self.set_invalid()


    @property
    def response(self) -> Response:
        """
        ========================================================================
         Return Response object.
        ========================================================================
        """
        return self._response

    def elapsed(self) -> float:
        """
        ========================================================================
         Get the time taken to receive the response (in seconds).
        ========================================================================
        """
        return self._elapsed

    def status(self) -> int:
        """
        ========================================================================
         Get the HTTP status code of the response.
        ========================================================================
        """
        return self._response.status_code

    def to_text(self) -> str:
        """
        ========================================================================
         Convert response content to text.
        =======================================================================
        """
        return self._response.text if self._response else None

    def to_dict(self) -> dict:
        """
        ========================================================================
         Convert response content to dictionary.
        ========================================================================
        """
        text = self.to_text()
        return json.loads(s=text) if text else None

    def to_json(self, path: str) -> None:
        """
        ========================================================================
         Save response content to list JSON file.
        ========================================================================
        """
        data = self.to_dict()
        with open(path, 'w') as file:
            json.dump(data, file, indent=4)

    def _request(self) -> None:
        """
        ========================================================================
         Make HTTP GET request and store the response and response time.
        ========================================================================
        """
        time_start = time.time()
        try:
            self._response = request('GET',
                                     self._url,
                                     params=self._params,
                                     headers=self._headers)
            self._elapsed = time.time() - time_start
        except Exception as e:
            self._response = None
            self._elapsed = None
            print(f'Request failed: {e}')

    def __str__(self) -> str:
        """
        ========================================================================
         Ex: {'music_id': '123', 'count': '20', 'cursor': '20'} ->
             is_valid=True, elapsed=1.08
        ========================================================================
        """
        return (f'{self._params} -> is_valid={bool(self)},'
                f' elapsed={self.elapsed()}')
