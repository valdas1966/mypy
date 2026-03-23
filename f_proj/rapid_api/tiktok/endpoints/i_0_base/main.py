from f_proj.rapid_api.tiktok.fetch.i_0_base import FetchBase
from f_proj.rapid_api.tiktok.fetch.i_1_single import FetchSingle
from f_proj.rapid_api.tiktok.fetch.i_1_multi import FetchMulti
from typing import Any, Callable


class Endpoint:
    """
    ============================================================================
     Base Class for TikTok API Endpoints.
    ============================================================================
     Subclasses define config (_path, _name_list, _name_cursor) and
     implement _params(), _anchor(), _to_row(). The run() logic is
     handled here — zero boilerplate in subclasses.
    ============================================================================
    """

    _path: str
    _name_list: str = None
    _name_cursor: str = 'cursor'
    _stop_if: Callable[[dict[str, Any]], bool] = None

    def _params(self) -> dict[str, Any]:
        """
        ====================================================================
         Build the params dict for the API call.
        ====================================================================
        """
        raise NotImplementedError

    def _anchor(self) -> tuple[str, str]:
        """
        ====================================================================
         Return the anchor tuple to identify the request.
        ====================================================================
        """
        raise NotImplementedError

    def _to_row(self, item: dict[str, Any]) -> dict[str, Any]:
        """
        ====================================================================
         Map an API response item to an output row.
        ====================================================================
        """
        raise NotImplementedError

    def run(self, limit: int = None) -> list[dict[str, Any]]:
        """
        ====================================================================
         Execute the endpoint fetch.
        ====================================================================
        """
        url = f'https://{FetchBase._HOST}/{self._path}'
        if self._name_list is None:
            return FetchSingle.run(url=url,
                                   params=self._params(),
                                   anchor=self._anchor(),
                                   to_row=self._to_row)
        return FetchMulti.run(url=url,
                              params=self._params(),
                              anchor=self._anchor(),
                              name_list=self._name_list,
                              to_row=self._to_row,
                              name_cursor=self._name_cursor,
                              limit=limit,
                              stop_if=self._stop_if)
