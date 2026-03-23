from f_proj.rapid_api.tiktok.endpoints.i_0_base import Endpoint
from typing import Any


class EndpointFollowersByUser(Endpoint):
    """
    ============================================================================
     Fetch Followers by User ID.
    ============================================================================
    """

    _path = 'user/followers'
    _name_list = 'followers'
    _name_cursor = 'time'

    def __init__(self, id_user: str) -> None:
        self._id_user = id_user

    def _params(self) -> dict[str, Any]:
        return {'user_id': self._id_user, 'count': 50, 'time': 0}

    def _anchor(self) -> tuple[str, str]:
        return ('id_user', self._id_user)

    def _to_row(self, item: dict[str, Any]) -> dict[str, Any]:
        return {'id_user': self._id_user,
                'id_follower': item['id'],
                'id_user_unique': item['unique_id'],
                'nick': item['nickname'],
                'region': item['region'],
                'is_verified': item['verified'],
                'is_secret': item['secret'],
                'followers': item['follower_count'],
                'following': item['following_count'],
                'aweme': item['aweme_count'],
                'favorited': item['total_favorited']}
