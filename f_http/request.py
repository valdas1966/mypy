from f_http.response import ResponseAPI
import requests

class RequestGet:
    """
    ========================================================================
     Class for sending Http-Requests.
    ========================================================================
    """

    @staticmethod
    def get(url: str,
            params: dict[str, str] = None,
            headers: dict[str, str] = None,
            ) -> ResponseAPI:
        """
        ========================================================================
         Send a GET request to the specified URL and return the response.
        ========================================================================
        """
        try:
            response = requests.get(url, params=params, headers=headers)
            data: dict = None
            try:
                data = response.json()
            except:
                pass
            status = response.status_code
            elapsed = round(response.elapsed.total_seconds(), 2)
            return ResponseAPI(data=data, status=status, elapsed=elapsed)
        except requests.exceptions.RequestException as e:
            return ResponseAPI(data=None, status=None, elapsed=None)
