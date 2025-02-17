from __future__ import annotations
from collections import namedtuple
from f_proj.rapid_api.requests.base import RequestBase


class Music(RequestBase):
    """
    ============================================================================
     Funcs to get Tiktok-Data by Music-Id.
    ============================================================================
    """

    Videos = namedtuple(typename='Videos',
                        field_names=['json', 'cursor', 'has_more', 'videos'])

    def get_videos(self,
                   id_hashtag: str,
                   cursor: str = '0') -> Music.Videos:
        """
        ========================================================================
         Return 20 Videos with a given Music-Id.
        ========================================================================
        """
        url = f'https://{self._host}/music/posts'
        params = {'music_id': id_music, 'count': '20', 'cursor': cursor}
        response = self.request(url=url, params=params)
        if response:
            json = response.to_dict()
            data = json['data']
            cursor = data['cursor']
            has_more = data['hasMore']
            videos = data['videos']
            return Music.Videos(json, cursor, has_more, videos)
