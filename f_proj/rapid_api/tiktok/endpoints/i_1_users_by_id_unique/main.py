from f_proj.rapid_api.tiktok.endpoints.i_0_base import Endpoint
from typing import Any


class EndpointUsersByIdUnique(Endpoint):
    """
    ============================================================================
     Fetch Users by Unique ID.
    ============================================================================
    """

    _path = 'user/info'

    def __init__(self, id_user_unique: str) -> None:
        self._id_user_unique = id_user_unique

    def _params(self) -> dict[str, Any]:
        return {'unique_id': f'@{self._id_user_unique}',
                'id_user_unique': self._id_user_unique}

    def _anchor(self) -> tuple[str, str]:
        return ('id_user_unique', self._id_user_unique)

    def _to_row(self, item: dict[str, Any]) -> dict[str, Any]:
        return {'id_user_unique': self._id_user_unique,
                'id_user': item['user']['id'],
                'nick': item['user']['nickname'],
                'is_verified': item['user']['verified'],
                'is_secret': item['user']['secret'],
                'is_private': item['user']['privateAccount'],
                'videos': item['stats']['videoCount'],
                'hearts': item['stats']['heartCount'],
                'diggs': item['stats']['diggCount'],
                'followers': item['stats']['followerCount'],
                'following': item['stats']['followingCount'],
                'is_found': True}
