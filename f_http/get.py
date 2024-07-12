from requests import request, Response
import json
import time


class GetRequest:
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
        self._url: str = url
        self._params: dict[str, str] = params or dict()
        self._headers: dict[str, str] = headers or dict()
        self._response: Response | None = None
        self._elapsed: float | None = None
        self._request()

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

    def is_valid(self) -> bool:
        """
        ========================================================================
         Check if the response is valid (status code 200).
        ========================================================================
        """
        return self._response is not None and self._response.status_code == 200

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
         Save response content to a JSON file.
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
