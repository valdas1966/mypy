from typing import Any
from f_os import u_environ
from f_http.request import RequestGet, ResponseAPI


class TiktokAPI:
    """
    ============================================================================
     Class for TikTok-API on Rapid-API.
    ============================================================================
    """

    _HOST = 'tiktok-video-no-watermark2.p.rapidapi.com'
    _KEY = u_environ.get('TIKTOK_1')
    # _KEY = '78e3c6307bmsh3e0d2026acb75dep1446a5jsn20b3e7f2a363'
    _HEADERS: dict[str, str] = {'X-RapidAPI-Host': _HOST,
                                'X-RapidAPI-Key': _KEY}
    

    @staticmethod
    def users_by_id(id_user: str) -> dict[str, Any]:
        """
        ========================================================================
         Fetch users by their ids.
        ========================================================================
        """
        url = 'https://tiktok-video-no-watermark2.p.rapidapi.com/user/info'
        params = {'user_id': id_user}
        response: ResponseAPI = RequestGet.get(url=url,
                                               params=params,
                                               headers=TiktokAPI._HEADERS)
        row: dict[str, Any] = {'id_user': id_user}
        if response:
            row['is_ok'] = True
            if response.is_found:
                row['is_found'] = True
                if row['is_ok'] and row['is_found']:
                    try:
                        d_user = response.data['data']['user']
                        row['id_user_unique'] = d_user['uniqueId']
                        row['nick'] = d_user['nickname']
                        row['is_verified'] = d_user['verified']
                        row['is_secret'] = d_user['secret']
                        row['is_private'] = d_user['privateAccount']
                        d_stats = response.data['data']['stats']
                        row['following'] = d_stats['followingCount']
                        row['followers'] = d_stats['followerCount']
                        row['videos'] = d_stats['videoCount']
                        row['hearts'] = d_stats['heartCount']
                        row['diggs'] = d_stats['diggCount']
                        row['is_broken'] = False                            
                    except Exception as e:
                        print(e)
                        row['is_broken'] = True
            else:
                row['is_found'] = False
        else:
            row['is_ok'] = False                                            
        return row
