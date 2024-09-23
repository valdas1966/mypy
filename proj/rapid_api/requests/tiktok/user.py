from collections import namedtuple
from proj.rapid_api.requests.base import RequestBase


class User(RequestBase):
    """
    ============================================================================
     Funcs to get Tiktok-Data by User-Id.
    ============================================================================
    """

    ResInfo = namedtuple(typename='ResInfo',
                         field_names=['id', 'nick', 'following', 'followers',
                                      'is_exist', 'is_valid'])

    ResFollower = namedtuple(typename='ResInfo',
                             field_names=['id', 'nick', 'region', 'verified',
                                          'secret', 'aweme', 'favorited',
                                          'following', 'followers'])

    def info(self, id_user: str) -> ResInfo:
        """
        ========================================================================
         Return User-Info.
        ========================================================================
        """
        url = f'https://{self._host}/user/info'
        params = {'user_id': id_user}
        d = self.request(url, params).to_dict()
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

    def followers(self,
                  id_user: str,
                  verbose: bool = True) -> list[dict] | None:
        """
        ========================================================================
         Return User-Info.
        ========================================================================
        """
        url = f'https://{self._host}/user/followers'
        params = {'user_id': id_user, 'count': '50'}
        d = self.request(url, params).to_dict()
        is_valid = d['code'] == 0
        is_exist = d['msg'] == 'success'
        li = None   
        if is_valid and is_exist:
            li = list()
            data = d['data']['followers']
            for follower in data:
                rec = dict()
                rec['id_user'] = id_user
                rec['id_follower'] = follower['id']
                rec['nick'] = follower['nickname']
                rec['region'] = follower['region']
                rec['verified'] = follower['verified']
                rec['secret'] = follower['secret']
                rec['aweme'] = follower['aweme_count']
                rec['favorited'] = follower['total_favorited']
                rec['following'] = follower['following_count']
                rec['followers'] = follower['follower_count']
                li.append(rec)
        if verbose:
            if li is None:
                print(f'Error in extracting followers of {id_user}')
            else:
                print(f'Extracted {len(li)} followers of {id_user}')
        return li
