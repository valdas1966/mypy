from f_proj.rapid_api.tiktok.fetch.i_0_base import FetchBase
from f_proj.rapid_api.tiktok.fetch.i_1_multi._batch import Batch
from typing import Any, Callable


class FetchMulti(FetchBase):
    """
    ============================================================================
     Fetch Multiple Items (Paginated) from TikTok RapidAPI.
    ============================================================================
    """

    @staticmethod
    def run(# URL to fetch the data from
            url: str,
            # Parameters to send to the API
            params: dict[str, Any],
            # Anchor to identify the request
            anchor: tuple[str, str],
            # Name of the list in the data (like videos, musics)
            name_list: str,
            # Function to convert a single item to a row
            to_row: Callable[[dict[str, Any]], dict[str, Any]],
            # Name of the cursor in the data
            name_cursor: str = 'cursor',
            # Limit of first rows to fetch
            limit: int = 100_000,
            # Optional early-termination condition
            stop_if: Callable[[dict[str, Any]], bool] = None
            ) -> list[dict[str, Any]]:
        """
        ====================================================================
         Fetch multiple items from the API (paginated).
        ====================================================================
        """
        limit = limit if limit else 100_000
        batch: Batch = Batch()
        rows_added: int = 1
        rows: list[dict[str, Any]] = list()
        while batch.has_more and rows_added:
            rows_added = 0
            params[name_cursor] = batch.cursor
            response = FetchMulti._get_response(url=url,
                                                params=params)
            if not response:
                return [FetchMulti._on_error(
                    status=response.status, anchor=anchor)]
            try:
                batch = FetchMulti._next_batch(
                    data=response.data['data'],
                    name_list=name_list,
                    name_cursor=name_cursor)
                for item in batch.items:
                    row = FetchMulti._stamp(to_row(item))
                    # Check early-termination condition
                    if stop_if and stop_if(row):
                        return rows
                    rows.append(row)
                    rows_added += 1
                if len(rows) >= limit:
                    return rows
            except Exception as e:
                return [FetchMulti._on_broken(msg=str(e),
                                             anchor=anchor)]
        return rows

    @staticmethod
    def _next_batch(# Response-Data from the API (json-dict)
                    data: dict[str, Any],
                    # Name of the list in the data
                    name_list: str,
                    # Name of the cursor in the data
                    name_cursor: str = 'cursor') -> Batch:
        """
        ====================================================================
         Get the next batch of data from the API.
        ====================================================================
        """
        has_more: bool = data['hasMore']
        cursor: str = data[name_cursor]
        items: list[dict[str, Any]] = data[name_list]
        return Batch(items=items, has_more=has_more, cursor=cursor)
