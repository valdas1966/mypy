from f_proj.rapid_api.tiktok.endpoints.i_0_base import Endpoint
from typing import Any


class EndpointHashtagsByKeyword(Endpoint):
    """
    ============================================================================
     Fetch Hashtags by Keyword.
    ============================================================================
    """

    _path = 'challenge/search'
    _name_list = 'challenge_list'

    def __init__(self, keyword: str) -> None:
        self._keyword = keyword

    def _params(self) -> dict[str, Any]:
        return {'keywords': self._keyword, 'count': 50,
                'cursor': 0}

    def _anchor(self) -> tuple[str, str]:
        return ('keyword', self._keyword)

    def _to_row(self, item: dict[str, Any]) -> dict[str, Any]:
        return {'keyword': self._keyword,
                'id_hashtag': item['id'],
                'hashtag': item['cha_name'],
                'users': item['user_count'],
                'views': item['view_count']}
