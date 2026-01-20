from f_http.client.client import Client, Response, Status
from f_proj.rapid_api.tiktok.batch import Batch
from f_utils import u_file
from f_psl.sys import utils
from pathlib import Path
from f_os import u_environ
from typing import Any, Callable


class TiktokAPI:
    """
    ============================================================================
     Class for TikTok-API on Rapid-API.
    ============================================================================
    """

    _PATH_MAC = str(Path.home() / 'prof' / 'rapid_tiktok.txt')
    _HOST = 'tiktok-video-no-watermark2.p.rapidapi.com'
    _KEY = u_file.read(_PATH_MAC) if utils.is_mac() else u_environ.get('TIKTOK_1')
    _HEADERS: dict[str, str] = {'X-RapidAPI-Host': _HOST,
                                'X-RapidAPI-Key': _KEY}


    @staticmethod
    def fetch_single(# URL to fetch the data from
                     url: str,
                     # Parameters to send to the API
                     params: dict[str, Any],
                     # Anchor to identify the request (like id_user, 122343434)
                     anchor: tuple[str, str],
                     # Function to convert the data to a row (dict to dict)
                     to_row: Callable[[dict], dict]) -> dict[str, Any]:
        """
        ========================================================================
         Fetch a single item from the API.
        ========================================================================
        """
        # Fetch the data
        response = TiktokAPI._get_response(url=url, params=params)
        # If response is invalid, return an invalid dict
        if not response:
            return TiktokAPI._on_error(status=response.status, anchor=anchor)
        # Try to extract the data (json-dict)
        try:
            # Get the data (json-dict)
            data = response.data['data']
            # Convert the data to the desired format (dict)
            return to_row(item=data)
        # On error in fetching data, return a broken dict
        except Exception as e:
            return TiktokAPI._on_broken(msg=str(e), anchor=anchor)

    @staticmethod
    def fetch_multi(# URL to fetch the data from
                    url: str,
                    # Parameters to send to the API
                    params: dict[str, Any],
                    # Anchor to identify the request (like id_user, 122343434)
                    anchor: tuple[str, str],
                    # Name of the list in the data (like videos, musics)
                    name_list: str,
                    # Function to convert the json-data to a list of dicts
                    to_rows: Callable[[list[dict[str, Any]]], list[dict[str, Any]]],
                    # Name of the cursor in the data (cursor, time)
                    name_cursor: str = 'cursor',
                    # Limit of firstrows to fetch
                    limit: int = 100_000) -> list[dict[str, Any]]:
        """
        ========================================================================
         Fetch multiple items from the API and convert them to a list of dicts.
        ========================================================================
        """
        limit = limit if limit else 100_000
        # Batch of data from the API (data, has_more, cursor)
        batch: Batch = Batch()
        # Number of rows added (to avoid infinite loop)
        rows_added: int = 1
        # List of rows to return
        rows: list[dict[str, Any]] = list()
        # Fetch data while there is more data to fetch and rows were added
        while batch.has_more and rows_added:
            # Reset the number of rows added
            rows_added = 0
            # Update the cursor in the params that will be sent to the API
            params[name_cursor] = batch.cursor
            # Fetch the data
            response = TiktokAPI._get_response(url=url, params=params)
            # If response is invalid, return an invalid dict
            if not response:
                return [TiktokAPI._on_error(status=response.status, anchor=anchor)]
            # Try to extract the data
            try:
                # Fetch the next batch of data
                batch = TiktokAPI._next_batch(data=response.data['data'],
                                              name_list=name_list,
                                              name_cursor=name_cursor)
                # Convert the data to the desired format (list of dicts)
                rows_new = to_rows(items=batch.items)
                # Add the new rows to the list
                rows.extend(rows_new)
                # If the limit is reached, return the list
                if len(rows) >= limit:
                    return rows
                # Update the number of rows added
                rows_added += len(rows_new)
            # On error in fetching data, return a broken dict
            except Exception as e:
                return [TiktokAPI._on_broken(msg=str(e), anchor=anchor)]
        # Return the list of rows
        return rows
        
    @staticmethod
    def _get_response(# URL to fetch the data from
                      url: str,
                      # Parameters to send to the API
                      params: dict[str, Any]) -> Response:
        """
        ========================================================================
         Get the response from the API.
        ========================================================================
        """
        response = Client.get_json(url=url,
                                   params=params,
                                   headers=TiktokAPI._HEADERS)
        return response

    @staticmethod
    def _next_batch(# Response-Data from the API (json-dict)
                    data: dict[str, Any],
                    # Name of the list in the data (like videos, musics)
                    name_list: str,
                    # Name of the cursor in the data
                    name_cursor: str = 'cursor') -> Batch:
        """
        ========================================================================
         Get the next batch of data from the API.
        ========================================================================
        """
        has_more: bool = data['hasMore']
        cursor: str = data[name_cursor]
        items: list[dict[str, Any]] = data[name_list]
        return Batch(items=items, has_more=has_more, cursor=cursor)

    @staticmethod
    def _on_error(# Status code of the response
                  status: Status,
                  # Anchor to identify the request (id_user, 122343434)
                  anchor: tuple[str, str]) -> dict[str, Any]:
        """
        ========================================================================
         Generate an invalid dict.
        ========================================================================
        """
        return {'status_code': status.code,
                'is_ok': False,
                anchor[0]: anchor[1]}
    
    @staticmethod
    def _on_broken(# Message of the error
                   msg: str,
                   # Anchor to identify the request (id_user, 122343434)
                   anchor: tuple[str, str]) -> dict[str, Any]:
        """
        ========================================================================
         Generate a broken dict.
        ========================================================================
        """
        return {'is_ok': True,
                'is_broken': True,
                'msg': msg,
                anchor[0]: anchor[1]}
