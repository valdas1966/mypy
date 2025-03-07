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

    @staticmethod
    def videos_by_user(id_user: str) -> list[dict[str, Any]]:
        """
        ========================================================================
         Fetch videos by user id.
        ========================================================================
        """
        url = 'https://tiktok-video-no-watermark2.p.rapidapi.com/user/posts'
        has_more = True
        cursor = 0
        rows_added = 1
        rows: list[dict[str, Any]] = list()
        while has_more and rows_added:
            rows_added = 0
            params = {'user_id': id_user, 'count': 50, 'cursor': cursor}
            response: ResponseAPI = RequestGet.get(url=url,
                                                   params=params,
                                                   headers=TiktokAPI._HEADERS)
            if response:
                if response.is_found:
                    try:
                        code = response.data['code']
                        msg = response.data['msg']
                        cursor = response.data['data']['cursor']
                        has_more = response.data['data']['hasMore']
                        for d in response.data['data']['videos']:
                            row: dict[str, Any] = {'id_user': id_user,
                                                   'status_code': code,
                                                   'msg': msg,
                                                   'is_ok': True,
                                                   'is_found': True}
                            row['id_music'] = d['music_info']['id']
                            row['id_video'] = d['video_id']
                            row['created'] = d['create_time']
                            row['region'] = d['region']
                            row['title'] = d['title']
                            row['duration'] = d['duration']
                            row['plays'] = d['play_count']
                            row['shares'] = d['share_count']
                            row['diggs'] = d['digg_count']
                            row['comments'] = d['comment_count']
                            row['downloads'] = d['download_count']
                            row['is_ad'] = d['is_ad']
                            row['play'] = d['play']
                            row['is_broken'] = False
                            rows.append(row)
                            rows_added += 1
                    except Exception:
                        row = {'id_user': id_user,
                               'status_code': code,
                               'msg': msg,
                               'is_ok': True,
                               'is_found': True,
                               'is_broken': True}
                        rows.append(row)
                else:
                    row = {'id_user': id_user,
                           'status_code': response.status,
                           'is_ok': True,
                           'is_found': False}
                    rows.append(row)
            else:
                row = {'id_user': id_user,
                       'status_code': response.status,
                       'is_ok': False}
                rows.append(row)
        return rows

    @staticmethod
    def videos_by_music(id_music: str) -> list[dict[str, Any]]:
        """
        ========================================================================
         Fetch videos by music id.
        ========================================================================
        """
        url = f'https://{TiktokAPI._HOST}/music/posts'
        has_more = True
        cursor = 0
        rows_added = 1
        rows: list[dict[str, Any]] = list()
        while has_more and rows_added:
            rows_added = 0
            params = {'music_id': id_music, 'count': 50, 'cursor': cursor}
            response: ResponseAPI = RequestGet.get(url=url,
                                                   params=params,
                                                   headers=TiktokAPI._HEADERS)
            if response:
                if response.is_found:
                    try:
                        code = response.data['code']
                        msg = response.data['msg']
                        cursor = response.data['data']['cursor']
                        has_more = response.data['data']['hasMore']
                        for d in response.data['data']['videos']:
                            row: dict[str, Any] = {'id_music': id_music,
                                                   'status_code': code,
                                                   'msg': msg,
                                                   'is_ok': True,
                                                   'is_found': True}
                            row['id_video'] = d['video_id']
                            row['id_user'] = d['author']['id']
                            row['is_broken'] = False
                            rows.append(row)
                            rows_added += 1
                    except Exception:
                        row = {'id_music': id_music,
                               'status_code': code,
                               'msg': msg,
                               'is_ok': True,
                               'is_found': True,
                               'is_broken': True}
                        rows.append(row)
                else:
                    row = {'id_music': id_music,
                           'status_code': response.status,
                           'is_ok': True,
                           'is_found': False}
                    rows.append(row)
            else:
                row = {'id_music': id_music,
                       'status_code': response.status,
                       'is_ok': False}
                rows.append(row)
            if len(rows) > 100000:
                return rows
        return rows

    @staticmethod
    def comments_by_video(id_video: str) -> list[dict[str, Any]]:
        """
        ========================================================================
         Fetch comments by video id.
        ========================================================================
        """
        url = f'https://{TiktokAPI._HOST}/comment/list'
        has_more = True
        cursor = 0
        rows_added = 1
        rows: list[dict[str, Any]] = list()
        while has_more and rows_added:
            rows_added = 0
            params = {'url': f'https://www.tiktok.com/@tiktok/video/{id_video}',
                      'count': 50,
                      'cursor': cursor}
            response: ResponseAPI = RequestGet.get(url=url,
                                                   params=params,
                                                   headers=TiktokAPI._HEADERS)
            if response:
                if response.is_found:
                    try:
                        code = response.data['code']
                        msg = response.data['msg']
                        cursor = response.data['data']['cursor']
                        has_more = response.data['data']['hasMore']
                        for d in response.data['data']['comments']:
                            row: dict[str, Any] = {'id_video': id_video,
                                                   'status_code': code,
                                                   'msg': msg,
                                                   'is_ok': True,
                                                   'is_found': True}
                            row['id_comment'] = d['id']
                            row['text'] = d['text']
                            row['replies'] = d['reply_total']
                            row['diggs'] = d['digg_count']
                            row['created'] = d['create_time']
                            row['id_user'] = d['user']['id']
                            row['id_user_unique'] = d['user']['unique_id']
                            row['nick'] = d['user']['nickname']
                            row['region'] = d['user']['region']
                            row['aweme'] = d['user']['aweme_count']
                            row['favorited'] = d['user']['total_favorited']
                            row['followers'] = d['user']['follower_count']
                            row['following'] = d['user']['following_count']
                            row['is_broken'] = False
                            rows.append(row)
                            rows_added += 1
                    except Exception:
                        row = {'id_video': id_video,
                               'status_code': code,
                               'msg': msg,
                               'is_ok': True,
                               'is_found': True,
                               'is_broken': True}
                        rows.append(row)
                else:
                    row = {'id_video': id_video,
                           'status_code': response.status,
                           'is_ok': True,
                           'is_found': False}
                    rows.append(row)
            else:
                row = {'id_video': id_video,
                       'status_code': response.status,
                       'is_ok': False}
                rows.append(row)
            if len(rows) > 100000:
                return rows
        return rows
