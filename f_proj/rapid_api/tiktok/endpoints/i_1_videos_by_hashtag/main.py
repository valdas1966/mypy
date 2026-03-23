from f_proj.rapid_api.tiktok.endpoints.i_0_base import Endpoint
from typing import Any


class EndpointVideosByHashtag(Endpoint):
    """
    ============================================================================
     Fetch Videos by Hashtag ID.
    ============================================================================
    """

    _path = 'challenge/posts'
    _name_list = 'videos'

    def __init__(self, id_hashtag: str) -> None:
        self._id_hashtag = id_hashtag

    def _params(self) -> dict[str, Any]:
        return {'challenge_id': self._id_hashtag, 'count': 50,
                'cursor': 0}

    def _anchor(self) -> tuple[str, str]:
        return ('id_hashtag', self._id_hashtag)

    def _to_row(self, item: dict[str, Any]) -> dict[str, Any]:
        return {'id_hashtag': self._id_hashtag,
                'id_user': item['author']['id'],
                'id_user_unique': item['author']['unique_id'],
                'nick': item['author']['nickname'],
                'id_video': item['video_id'],
                'region': str(item['region']),
                'title': item['title'],
                'created': item['create_time'],
                'duration': item['duration'],
                'plays': item['play_count'],
                'shares': item['share_count'],
                'diggs': item['digg_count'],
                'comments': item['comment_count'],
                'downloads': item['download_count'],
                'is_ad': item['is_ad'],
                'play': item['play']}
