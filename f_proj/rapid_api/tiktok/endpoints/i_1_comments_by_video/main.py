from f_proj.rapid_api.tiktok.endpoints.i_0_base import Endpoint
from typing import Any


class EndpointCommentsByVideo(Endpoint):
    """
    ============================================================================
     Fetch Comments by Video ID.
    ============================================================================
    """

    _path = 'comment/list'
    _name_list = 'comments'

    def __init__(self, id_video: str) -> None:
        self._id_video = id_video

    def _params(self) -> dict[str, Any]:
        return {'url': (f'https://www.tiktok.com/@tiktok/'
                        f'video/{self._id_video}'),
                'count': 50,
                'cursor': 0}

    def _anchor(self) -> tuple[str, str]:
        return ('id_video', self._id_video)

    def _to_row(self, item: dict[str, Any]) -> dict[str, Any]:
        return {'id_video': self._id_video,
                'id_comment': item['id'],
                'text': item['text'],
                'replies': item['reply_total'],
                'diggs': item['digg_count'],
                'created': item['create_time'],
                'id_user': item['user']['id'],
                'id_user_unique': item['user']['unique_id'],
                'nick': item['user']['nickname'],
                'region': item['user']['region'],
                'aweme': item['user']['aweme_count'],
                'favorited': item['user']['total_favorited'],
                'followers': item['user']['follower_count'],
                'following': item['user']['following_count']}
