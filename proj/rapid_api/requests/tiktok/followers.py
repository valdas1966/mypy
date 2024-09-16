from f_utils import u_http_requests
from collections import namedtuple


class Followers:
    """
    ============================================================================
     Funcs to get Tiktok-User Followers.
    ============================================================================
    """

    ResInfo = namedtuple(typename='ResInfo',
                         field_names=['id', 'unique', 'nick',
                                      'region', 'following',
                                      'following', 'followers'])

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
        """
        ========================================================================
         Return User-Info.
        ========================================================================
        """
        url = f'https://{self._host}/user/info'
        params = {'user_id': id_user}
        d = u_http_requests.get_dict(url, params, self._headers)
        is_valid = d['code'] == 0
        is_exist = d['msg'] == 'success'
        id_user = None
        nick = None
        following = None
        followers = None
        if is_valid and is_exist:
            data = d['data']
            id_user = data['user']['id']
            nick = data['user']['nickname']
            following = data['stats']['followingCount']
            followers = data['stats']['followerCount']
        return self.ResInfo(id=id_user,
                            nick=nick,
                            following=following,
                            followers=followers,
                            is_exist=is_exist,
                            is_valid=is_valid)
