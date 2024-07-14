from __future__ import annotations
from f_http.get import Get
from collections import namedtuple


class Music:
    """
    ============================================================================
     Funcs to get Tiktok-Data by Music-Id.
    ============================================================================
    """

    Videos = namedtuple(typename='Videos',
                        field_names=['cursor', 'has_more', 'videos'])

    def __init__(self,
                 key: str,
                 host: str,
                 headers: dict[str, str]) -> None:
        """
        ========================================================================
         Init private Attributes.
        ========================================================================
        """
        self._key = key
        self._host = host
        self._headers = headers

    def get_videos(self,
                   id_music: str,
                   cursor: str = '20') -> Music.Videos:
        """
        ========================================================================
         Return 20 Videos with given Music-Id.
        ========================================================================
        """
        url = f'https://{self._host}/music/posts'
        params = {'music_id': id_music, 'count': '20', 'cursor': cursor}
        response = Get(url, params, self._headers)
        if response:
            d = response.to_dict()
            data = d['data']
            cursor = data['cursor']
            has_more = data['hasMore']
            videos = data['videos']
            return Music.Videos(cursor, has_more, videos)




