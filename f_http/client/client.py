from f_http.responses.json import ResponseJson
from f_http.responses.file import ResponseFile
from f_http.status.status import StatusHttp
from pathlib import Path
from typing import Any
import requests


class ClientHttp:
    """
    ============================================================================
     ClientHttp class for sending HTTP-GET requests (to get json-dict or file).
    ============================================================================
    """

    @staticmethod
    def get_json(# URL to send the GET request to
                 url: str,
                 # Parameters to be sent in the GET request
                 params: dict[str, Any] = None,
                 # Headers to be sent in the GET request
                 headers: dict[str, str] = None) -> ResponseJson:
        """
        ========================================================================
         Send an HTTP-GET request and parse the response to ResponseJson.
        ========================================================================
        """
        # Init the response variables as None (if request fails)
        status: StatusHttp | None = None
        data: dict[str, Any] | None = None        
        elapsed: float | None = None
        exception: str | None = None

        # Try to get the response from the URL and parse to ResponseJson
        try:
            response = requests.get(url=url, params=params, headers=headers)
            status = StatusHttp(code=response.status_code)
            elapsed = round(response.elapsed.total_seconds(), 2)
            if status.is_valid:
                data = response.json()
        except Exception as e:
            exception = str(e)

        # Return the parsed Response as ResponseJson
        return ResponseJson(status=status,
                            data=data,
                            elapsed=elapsed,
                            exception=exception)

    @staticmethod
    def get_file(# URL to send the GET request to
                 url: str,
                 # Destination path to save the file
                 dest: Path | str) -> ResponseFile:
        """
        ========================================================================
         Download a file from a URL to a destination path.
        ========================================================================
        """
        # Set dest as Path object
        dest: Path = dest if isinstance(dest, Path) else Path(dest)
        # Try to download the file
        try:
            # Try to get the response from the URL
            with requests.get(url=url, stream=True) as resp:
                # Get the elapsed time of the response
                elapsed = round(resp.elapsed.total_seconds(), 2)
                # If the response is not valid
                if resp.status_code != 200:
                    return ResponseFile(path=None,
                                        status = resp.status_code,
                                        elapsed = elapsed)
                # Create the parent directory if it doesn't exist
                dest.parent.mkdir(parents=True, exist_ok=True)
                size = 0
                with dest.open("wb") as fh:
                    for chunk_bytes in resp.iter_content(chunk):
                        if chunk_bytes:
                            fh.write(chunk_bytes)
                            size += len(chunk_bytes)
            return FileResponse(dest, size,
                                status = resp.status_code,
                                elapsed = elapsed)
        except (requests.RequestException, OSError) as exc:
            if dest.exists():
                dest.unlink(missing_ok=True)
            return FileResponse(None, None, status=None, elapsed=None)
