from typing import Any
from f_os import u_environ
from f_http.request import RequestGet, ResponseAPI
from f_proj.rapid_api.data.i_3_users_by_id import DataUsersById
from f_proj.rapid_api.data.i_0_audit import DataAudit
from f_proj.rapid_api.data.i_0_list import DataList
from f_proj.rapid_api.data.i_1_hashtag import DataHashtag


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
    def _fetch_single(url: str,
                      params: dict[str, Any],
                      data: DataAudit) -> dict[str, Any]:
        """
        ========================================================================
         Fetch a single item from the API.
        ========================================================================
        """
        response: ResponseAPI = RequestGet.get(url=url,
                                               params=params,
                                               headers=TiktokAPI._HEADERS)
        # Check if the response is ok.
        if not response:
            data.is_ok = False
            return data.to_flat_dict()
        # Check if the user is found.
        data.is_ok = True
        if not response.is_found:
            data.is_found = False
            return data.to_flat_dict()
        # Try fill the data.
        data.is_found = True
        try:
            data.fill(**response.data)
            data.is_broken = False
        except Exception as e:
            print(e)
            data.is_broken = True     
        finally:
            return data.to_flat_dict()
        
    @staticmethod
    def _fetch_multi(url: str,
                     params: dict[str, Any],
                     data: DataAudit) -> list[dict[str, Any]]:
        """
        ========================================================================
         Fetch multiple items from the API.
        ========================================================================
        """
        has_more = True
        cursor = 0
        rows_added = 1
        rows: list[dict[str, Any]] = list()
        while has_more and rows_added:
            d = data.model_copy()
            rows_added = 0
            params['cursor'] = cursor
            response: ResponseAPI = RequestGet.get(url=url,
                                                   params=params,
                                                   headers=TiktokAPI._HEADERS)
            # Check if the response is ok.
            if not response:
                d.is_ok = False
                row = d.to_flat_dict()
                rows.append(row)
                return rows
            # Check if the user is found.
            d.is_ok = True
            if not response.is_found:
                d.is_found = False
                row = d.to_flat_dict()
                rows.append(row)
                return rows
            # Try fill the data.
            d.is_found = True
            try:
                d.fill(**response.data)
                d.is_broken = False
            except Exception as e:
                print(e)
                d.is_broken = True     
            finally:
                row = d.to_flat_dict()
                rows.append(row)
                rows_added += 1
        return rows
        

    @staticmethod
    def users_by_id(id_user: str) -> dict[str, Any]:
        """
        ========================================================================
         Fetch users by their ids.
        ========================================================================
        """
        url = f'https://{TiktokAPI._HOST}/user/info'
        params = {'user_id': id_user}
        data = DataUsersById()
        data.id_user = id_user
        return TiktokAPI._fetch_single(url=url,
                                       params=params,
                                       data=data)

    @staticmethod
    def users_by_id_unique(id_user_unique: str) -> dict[str, Any]:
        """
        ========================================================================
         Fetch users by their unique ids.
        ========================================================================
        """
        url = f'https://{TiktokAPI._HOST}/user/info'
        params = {'unique_id': f'@{id_user_unique}'}
        data = DataUsersById()
        data.id_user_unique = id_user_unique
        return TiktokAPI._fetch_single(url=url,
                                       params=params,
                                       data=data)

    


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
