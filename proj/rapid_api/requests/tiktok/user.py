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

    def followers(self, id_user: str) -> list[ResInfo] | None:
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
                id_follower = follower['id']
                nick = follower['nickname']
                region = follower['region']
                verified = follower['verified']
                secret = follower['secret']
                aweme = follower['aweme_count']
                favorited = follower['total_favorited']
                following = follower['following_count']
                followers = follower['follower_count']
                res = self.ResFollower(id=id_follower,
                                       nick=nick,
                                       region=region,
                                       verified=verified,
                                       secret=secret,
                                       aweme=aweme,
                                       favorited=favorited,
                                       following=following,
                                       followers=followers)
                li.append(res)
        return li
