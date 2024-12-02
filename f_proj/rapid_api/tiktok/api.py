from f_os import u_environ
from f_proj.rapid_api.tiktok.data.user_snapshot import DataUserSnapshot
from f_http.get.request import RequestGet, Input, Reasons


class TiktokAPI:
    """
    ============================================================================
     Class for TikTok-API on Rapid-API.
    ============================================================================
    """

    _HOST = 'tiktok-video-no-watermark2.p.rapidapi.com'
    _KEY = u_environ.get('TIKTOK_1')
    _HEADERS: dict[str, str] = {'X-RapidAPI-Host': _HOST,
                                'X-RapidAPI-Key': _KEY}

    @staticmethod
    def user_snapshot(id_user: str) -> DataUserSnapshot:
        url = f'https://{TiktokAPI._HOST}/user/info'
        params = {'user_id': id_user}
        _input = Input(url=url, params=params, headers=TiktokAPI._HEADERS)
        request = RequestGet(_input=_input)
        output = request.run()
        data = DataUserSnapshot()
        if request:
            data.id_user = id_user
            data.is_ok = True
            try:
                d = output.to_dict()['data']
            except KeyError:
                data.is_found = False
                return data
            data.is_found = True
            d_user = d['user']
            data.nick = d_user['nickname']
            data.is_verified = d_user['verified']
            data.is_secret = d_user['secret']
            data.is_private = d_user['privateAccount']
            d_stats = d['stats']
            data.following = d_stats['followingCount']
            data.followers = d_stats['followerCount']
            data.videos = d_stats['videoCount']
            data.hearts = d_stats['heart']
            data.diggs = d_stats['diggCount']
        elif request.reason == Reasons.NOT_FOUND:
            data.is_ok = True
            data.is_found = False
        else:
            data.is_ok = False
        return data
