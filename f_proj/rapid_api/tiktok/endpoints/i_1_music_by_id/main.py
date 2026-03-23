from f_proj.rapid_api.tiktok.endpoints.i_0_base import Endpoint
from typing import Any


class EndpointMusicById(Endpoint):
    """
    ============================================================================
     Fetch Music by ID.
    ============================================================================
    """

    _path = 'music/info'

    def __init__(self, id_music: str) -> None:
        self._id_music = id_music

    def _params(self) -> dict[str, Any]:
        return {'url': self._id_music}

    def _anchor(self) -> tuple[str, str]:
        return ('id_music', self._id_music)

    def _to_row(self, item: dict[str, Any]) -> dict[str, Any]:
        return {'id_music': self._id_music,
                'title': item['title'],
                'play': item['play'],
                'author': item['author'],
                'duration': item['duration'],
                'is_original': item['original'],
                'videos': item['video_count']}
