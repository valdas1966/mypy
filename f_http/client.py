from f_http.inner.responses.json import ResponseJson
from f_http.inner.responses.file import ResponseFile
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
         Send an HTTP-GET request and parse the response body as ResponseJson.
        ========================================================================
        """
        try:
            # Try to get the response from the URL
            response = requests.get(url=url, params=params, headers=headers)
            # Get the elapsed time of the response
            elapsed = round(response.elapsed.total_seconds(), 2)
            try:
                # Try to parse the response body as JSON
                data = response.json()
            except ValueError:
                # Response is not JSON
                data = None
            # On valid JSON-Conversion: Return the ResponseJson object
            return ResponseJson(data=data,
                                status=response.status_code,
                                elapsed=elapsed)
        except requests.RequestException:
            # On error: Return invalid ResponseJson object
            return ResponseJson(data=None, status=None, elapsed=None)

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
