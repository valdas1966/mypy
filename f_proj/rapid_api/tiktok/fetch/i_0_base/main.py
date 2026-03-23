from f_http import Client, Response, Status
from f_utils import u_file
from f_psl.sys import utils
from pathlib import Path
from f_os import u_environ
from typing import Any


class FetchBase:
    """
    ============================================================================
     Base Configuration and Shared Helpers for TikTok RapidAPI.
    ============================================================================
    """

    _PATH_MAC = str(Path.home() / 'prof' / 'rapid_tiktok.txt')
    _HOST = 'tiktok-video-no-watermark2.p.rapidapi.com'
    _KEY = (u_file.read(_PATH_MAC) if utils.is_mac()
            else u_environ.get('TIKTOK_1'))
    _HEADERS: dict[str, str] = {'X-RapidAPI-Host': _HOST,
                                'X-RapidAPI-Key': _KEY}

    @staticmethod
    def _get_response(# URL to fetch the data from
                      url: str,
                      # Parameters to send to the API
                      params: dict[str, Any]) -> Response:
        """
        ====================================================================
         Get the response from the API.
        ====================================================================
        """
        return Client.get_json(url=url,
                               params=params,
                               headers=FetchBase._HEADERS)

    @staticmethod
    def _on_error(# Status code of the response
                  status: Status,
                  # Anchor to identify the request
                  anchor: tuple[str, str]) -> dict[str, Any]:
        """
        ====================================================================
         Generate an invalid dict.
        ====================================================================
        """
        return {'status_code': status.code,
                'is_ok': False,
                anchor[0]: anchor[1]}

    @staticmethod
    def _on_broken(# Message of the error
                   msg: str,
                   # Anchor to identify the request
                   anchor: tuple[str, str]) -> dict[str, Any]:
        """
        ====================================================================
         Generate a broken dict.
        ====================================================================
        """
        return {'is_ok': True,
                'is_broken': True,
                'msg': msg,
                anchor[0]: anchor[1]}

    @staticmethod
    def _stamp(row: dict[str, Any]) -> dict[str, Any]:
        """
        ====================================================================
         Stamp default status fields onto a row.
        ====================================================================
        """
        row['is_ok'] = True
        row['is_broken'] = False
        return row
