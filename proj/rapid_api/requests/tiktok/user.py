from proj.rapid_api.requests.base import RequestBase


class User(RequestBase):
    """
    ============================================================================
     Funcs to get Tiktok-Data by User-Id.
    ============================================================================
    """

    def info(self, id_user: str) -> dict:
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
        rec = dict()
        if is_valid and is_exist:
            rec['source'] = 'INFO'
            data = d['data']
            rec['id_user'] = data['user']['id']
            rec['nick'] = data['user']['nickname']
            rec['is_verified'] = data['user']['verified']
            rec['is_secret'] = data['user']['secret']
            rec['is_private'] = data['user']['privateAccount']
            rec['following'] = data['stats']['followingCount']
            rec['followers'] = data['stats']['followerCount']
            rec['videos'] = data['stats']['videoCount']
            rec['hearts'] = data['stats']['heart']
            rec['diggs'] = data['stats']['diggCount']
        else:
            print(f'Invalid Request: {id_user}')
        return rec

    def followers(self,
                  id_user: str,
                  time: int = 0) -> (list[dict], bool, int):
        """
        ========================================================================
         Return User-Info.
        ========================================================================
        """
        url = f'https://{self._host}/user/followers'
        params = {'user_id': id_user, 'count': '50', 'time': str(time)}
        d = self.request(url, params).to_dict()
        is_valid = d and d['code'] == 0
        is_exist = d and d['msg'] == 'success'
        has_more = False
        li = list()
        if is_valid and is_exist:
            has_more = d['data']['hasMore']
            time = d['data']['time']
            data = d['data']['followers']
            for follower in data:
                rec = dict()
                rec['id_user'] = id_user
                rec['id_follower'] = follower['id']
                rec['nick'] = follower['nickname']
                rec['region'] = follower['region']
                rec['is_verified'] = follower['verified']
                rec['is_secret'] = follower['secret']
                rec['aweme'] = follower['aweme_count']
                rec['favorited'] = follower['total_favorited']
                rec['following'] = follower['following_count']
                rec['followers'] = follower['follower_count']
                rec['source'] = 'FOLLOWERS'
                li.append(rec)
        print(f'Extracted {len(li)} followers of {id_user}')
        return li, has_more, time
