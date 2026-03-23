from f_proj.rapid_api.tiktok.endpoints.i_0_base import Endpoint
from typing import Any


class EndpointUsersById(Endpoint):
    """
    ============================================================================
     Fetch Users by Numeric ID.
    ============================================================================
    """

    _path = 'user/info'

    def __init__(self, id_user: str) -> None:
        self._id_user = id_user

    def _params(self) -> dict[str, Any]:
        return {'user_id': self._id_user}

    def _anchor(self) -> tuple[str, str]:
        return ('id_user', self._id_user)

    def _to_row(self, item: dict[str, Any]) -> dict[str, Any]:
        return {'id_user_unique': item['user']['uniqueId'],
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
                'signature': item['user']['signature'],
                'twitter': item['user']['twitter_id'],
                'youtube': item['user']['youtube_channel_title'],
                'avatar': item['user']['avatarMedium']}
