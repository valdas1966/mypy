from f_os import u_environ
from f_proj.rapid_api.tiktok.data.user_info import DataUserInfo
from f_proj.rapid_api.tiktok.data.response import DataResponse
from f_http.get.request import RequestGet, Input, Output, Reasons


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
    def user_info(id_user: str) -> DataResponse[DataUserInfo]:
        url = f'https://{TiktokAPI._HOST}/user/info'
        params = {'user_id': id_user}
        _input = Input(url=url, params=params, headers=TiktokAPI._HEADERS)
        request = RequestGet(_input=_input)
        output = request.run()
        data_response = DataResponse[DataUserInfo]()
        if request:
            data_user_info = DataUserInfo()
            d = output.to_dict()['data']
            d_user = d['user']
            data_user_info.id_user = d_user['id']
            data_user_info.nick = d_user['nickname']
            data_user_info.is_verified = d_user['verified']
            data_user_info.is_secret = d_user['secret']
            data_user_info.is_private = d_user['privateAccount']
            d_stats = d['stats']
            data_user_info.following = d_stats['followingCount']
            data_user_info.followers = d_stats['followerCount']
            data_user_info.videos = d_stats['videoCount']
            data_user_info.hearts = d_stats['heart']
            data_user_info.diggs = d_stats['diggCount']
            data_response.is_succeed = True
            data_response.is_found = True
            data_response.data = data_user_info
        elif request.reason == Reasons.NOT_FOUND:
            data_response.is_succeed = True
            data_response.is_found = False
        else:
            print(request.reason)
            data_response.is_succeed = False
        return data_response
