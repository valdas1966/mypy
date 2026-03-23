from f_proj.rapid_api.tiktok.endpoints.i_0_base import Endpoint
from typing import Any


class EndpointVideosByMusic(Endpoint):
    """
    ============================================================================
     Fetch Videos by Music ID.
    ============================================================================
    """

    _path = 'music/posts'
    _name_list = 'videos'

    def __init__(self, id_music: str) -> None:
        self._id_music = id_music

    def _params(self) -> dict[str, Any]:
        return {'music_id': self._id_music, 'count': 50,
                'cursor': 0}

    def _anchor(self) -> tuple[str, str]:
        return ('id_music', self._id_music)

    def _to_row(self, item: dict[str, Any]) -> dict[str, Any]:
        return {'id_music': self._id_music,
                'id_video': item['video_id'],
                'id_user': item['author']['id']}
