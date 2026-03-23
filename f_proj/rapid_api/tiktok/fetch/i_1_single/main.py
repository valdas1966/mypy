from f_proj.rapid_api.tiktok.fetch.i_0_base import FetchBase
from typing import Any, Callable


class FetchSingle(FetchBase):
    """
    ============================================================================
     Fetch a Single Item from TikTok RapidAPI.
    ============================================================================
    """

    @staticmethod
    def run(# URL to fetch the data from
            url: str,
            # Parameters to send to the API
            params: dict[str, Any],
            # Anchor to identify the request
            anchor: tuple[str, str],
            # Function to convert the data to a row
            to_row: Callable[[dict], dict]
            ) -> list[dict[str, Any]]:
        """
        ====================================================================
         Fetch a single item from the API.
        ====================================================================
        """
        response = FetchSingle._get_response(url=url,
                                             params=params)
        if not response:
            return [FetchSingle._on_error(status=response.status,
                                          anchor=anchor)]
        try:
            data = response.data['data']
            return [FetchSingle._stamp(to_row(data))]
        except Exception as e:
            return [FetchSingle._on_broken(msg=str(e),
                                           anchor=anchor)]
