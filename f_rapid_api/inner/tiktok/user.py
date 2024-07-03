from f_utils import u_http_requests
from collections import namedtuple


class User:
    """
    ============================================================================
     Funcs to get Tiktok-Data by User-Id.
    ============================================================================
    """

    ResInfo = namedtuple(typename='ResInfo',
                         field_names=['id', 'nick', 'following', 'followers',
                                      'is_exists', 'is_valid'])

    def __init__(self,
                 key: str,
                 host: str,
                 headers: dict[str, str]) -> None:
        """
        ========================================================================
         Init private Attributes.
        ========================================================================
        """
        self._key = key
        self._host = host
        self._headers = headers

    def info(self, id_user: str) -> ResInfo:
        url = f'{self._host}/user/info'
        params = {'user_id': id_user}
        d = u_http_requests.get_dict(url, params, self._headers)
        is_valid = d['code'] == 0
        is_exists = d['msg'] == 'success'
        id_user = None
        nick = None
        following = None
        followers = None
        if is_valid and is_exists:
            id_user = d['data']['id']
            nick = d['data']['nickname']
            following = d['stats']['followingCount']
            followers = d['stats']['followerCount']
        return self.ResInfo(id=id_user,
                            nick=nick,
                            following=following,
                            followers=followers,
                            is_exists=is_exists,
                            is_valid=is_valid)
