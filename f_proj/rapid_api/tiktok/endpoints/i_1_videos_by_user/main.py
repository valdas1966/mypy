from f_proj.rapid_api.tiktok.endpoints.i_0_base import Endpoint
from typing import Any


class EndpointVideosByUser(Endpoint):
    """
    ============================================================================
     Fetch Videos by User ID.
    ============================================================================
    """

    _path = 'user/posts'
    _name_list = 'videos'

    def __init__(self, id_user: str) -> None:
        self._id_user = id_user

    def _params(self) -> dict[str, Any]:
        return {'user_id': self._id_user, 'count': 50,
                'cursor': '0', 'id_user': self._id_user}

    def _anchor(self) -> tuple[str, str]:
        return ('id_user', self._id_user)

    def _to_row(self, item: dict[str, Any]) -> dict[str, Any]:
        return {'id_user': self._id_user,
                'id_music': item['music_info']['id'],
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
                'play': item['play'],
                'is_found': True}
