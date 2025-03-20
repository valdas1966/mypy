from typing import Any, Callable
from f_os import u_environ
from f_http.request import RequestGet, ResponseAPI
from typing import Type


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
        url = f'https://{TiktokAPI._HOST}/user/info'
        params = {'user_id': id_user}
        def to_row(data: dict[str, Any]) -> dict[str, Any]:
            row: dict[str, Any] = dict()
            row['id_user_unique'] = data['unique_id']
            row['id_user'] = data['user_id']
            row['nick'] = data['nickname']
            row['is_verified'] = data['verified']
            row['is_secret'] = data['secret']
            row['is_private'] = data['private']
            row['videos'] = data['video_count']
            row['hearts'] = data['heart_count']
            row['diggs'] = data['digg_count']
            row['followers'] = data['follower_count']
            row['following'] = data['following_count']
            row['is_ok'] = True
            row['is_found'] = True
            row['is_broken'] = False
            return row
        return TiktokAPI._fetch_single(url=url,
                                       params=params,
                                       anchor=('id_user', id_user),
                                       to_row=to_row)

    @staticmethod
    def users_by_id_unique(id_user_unique: str) -> dict[str, Any]:
        """
        ========================================================================
         Fetch users by their unique ids.
        ========================================================================
        """
        url = f'https://{TiktokAPI._HOST}/user/info'    
        params = {'unique_id': f'@{id_user_unique}',
                  'id_user_unique': id_user_unique}
        def to_row(data: dict[str, Any]) -> dict[str, Any]:
            row: dict[str, Any] = dict()
            row['id_user_unique'] = id_user_unique
            row['id_user'] = data['user_id']
            row['nick'] = data['nickname']
            row['is_verified'] = data['verified']
            row['is_secret'] = data['secret']
            row['is_private'] = data['private']
            row['videos'] = data['video_count']
            row['hearts'] = data['heart_count']
            row['diggs'] = data['digg_count']
            row['followers'] = data['follower_count']
            row['following'] = data['following_count']
            row['is_ok'] = True
            row['is_found'] = True
            row['is_broken'] = False
            return row
        return TiktokAPI._fetch_single(url=url,
                                       params=params,
                                       anchor=('id_user_unique', id_user_unique),
                                       to_row=to_row)

    @staticmethod
    def videos_by_user(id_user: str) -> list[dict[str, Any]]:
        """
        ========================================================================
         Fetch videos by user id.
        ========================================================================
        """
        url = 'https://tiktok-video-no-watermark2.p.rapidapi.com/user/posts'
        params = {'user_id': id_user, 'count': 50,
                  'cursor': 0, 'id_user': id_user}
        return TiktokAPI._fetch_multi(url=url,
                                      params=params,
                                      type_data=DataAudit,
                                      type_list=DataVideosByUser)

    @staticmethod
    def hashtags_by_keyword(keyword: str) -> list[dict[str, Any]]:
        """
        ========================================================================
         Fetch hashtags by keyword.
        ========================================================================
        """
        url = f'https://{TiktokAPI._HOST}/challenge/search'
        params = {'keywords': keyword, 'count': 50, 'cursor': 0}
        def to_rows(data: list[dict[str, Any]]) -> list[dict[str, Any]]:
            rows: list[dict[str, Any]] = list()
            for d in data:
                row: dict[str, Any] = dict()
                row['keyword'] = keyword
                row['id_hashtag'] = d['id']
                row['hashtag'] = d['cha_name']
                row['users'] = d['user_count']
                row['views'] = d['view_count']
                row['is_ok'] = True
                row['is_found'] = True
                row['is_broken'] = False
                rows.append(row)
            return rows
        return TiktokAPI._fetch_multi(url=url,
                                      params=params,
                                      anchor=('keyword', keyword),
                                      name_list='challenge_list',
                                      to_rows=to_rows)

    @staticmethod
    def videos_by_hashtag(id_hashtag: str) -> list[dict[str, Any]]:
        """
        ========================================================================
         Fetch videos by hashtag id.
        ========================================================================
        """ 
        url = f'https://{TiktokAPI._HOST}/challenge/posts'
        params = {'challenge_id': id_hashtag, 'count': 50, 'cursor': 0}
        def to_rows(data: list[dict[str, Any]]) -> list[dict[str, Any]]:
            rows: list[dict[str, Any]] = list()
            for d in data:
                row: dict[str, Any] = dict()
                row['id_hashtag'] = id_hashtag
                row['id_video'] = d['video_id']
                row['title'] = d['title']
                row['created'] = d['create_time']
                row['duration'] = d['duration']
                row['plays'] = d['play_count']
                row['shares'] = d['share_count']
                row['diggs'] = d['digg_count']
                row['comments'] = d['comment_count']
                row['downloads'] = d['download_count']
                row['is_ad'] = d['is_ad']
                row['play'] = d['play']
                row['is_ok'] = True
                row['is_found'] = True
                row['is_broken'] = False
                rows.append(row)
            return rows
        return TiktokAPI._fetch_multi(url=url,
                                      params=params,
                                      anchor=('id_hashtag', id_hashtag),
                                      name_list='videos',
                                      to_rows=to_rows)

    @staticmethod
    def _fetch_single(url: str,
                      params: dict[str, Any],
                      anchor: tuple[str, str],
                      to_row: Callable[[dict], dict]) -> dict[str, Any]:
        """
        ========================================================================
         Fetch a single item from the API.
        ========================================================================
        """
        # Shorthand
        cur = TiktokAPI
        # Fetch the data
        response: ResponseAPI = RequestGet.get(url=url, 
                                               params=params,
                                               headers=TiktokAPI._HEADERS)
        # If there is a problem with the response, return a not ok response
        if not response:
            return cur._gen_not_ok(status_code=response.status,
                                    anchor=anchor)
        # If the data is not found, return a not found response
        if not response.is_found:
            return cur._gen_not_found(anchor=anchor)
        # Try to extract the data
        try:
            # Get the data
            data = response.data['data']
            # Convert the data to the desired format (dict)
            return to_row(data=data)
        # If there is an error in fetching data, return a broken response
        except Exception as e:
            return cur._gen_broken(msg=str(e), anchor=anchor)

    @staticmethod
    def _fetch_multi(url: str,
                     params: dict[str, Any],
                     anchor: tuple[str, str],
                     name_list: str,
                     to_rows: Callable[[dict[str, Any]], list[dict[str, Any]]],
                     limit: int = 100000) -> list[dict[str, Any]]:
        """
        ========================================================================
         Fetch multiple items from the API.
        ========================================================================
        """
        # Shorthand
        cur = TiktokAPI
        # Has More data to fetch
        has_more = True
        # Cursor to start fetching from
        cursor = 0
        # Number of rows added (to avoid infinite loop)
        rows_added = 1
        # List of rows to return
        rows: list[dict[str, Any]] = list()
        # Fetch data while there is more data to fetch and rows were added
        while has_more and rows_added:
            # Reset the number of rows added
            rows_added = 0
            # Update the cursor in the params that will be sent to the API
            params['cursor'] = cursor
            # Fetch the data
            response: ResponseAPI = RequestGet.get(url=url, 
                                                   params=params,
                                                   headers=TiktokAPI._HEADERS)
            # If there is a problem with the response, return a not ok response
            if not response:
                return [cur._gen_not_ok(status_code=response.status,
                                        anchor=anchor)]
            # If the data is not found, return a not found response
            if not response.is_found:
                return [cur._gen_not_found(anchor=anchor)]
            # Try to extract the data
            try:
                data_list, has_more, cursor = cur._get_info(response=response,
                                                            name_list=name_list)
                # Convert the data to the desired format (list of dicts)
                rows_new = to_rows(data=data_list)
                # Add the new rows to the list
                rows.extend(rows_new)
                # If the limit is reached, return the list
                if len(rows) >= limit:
                    return rows
                # Update the number of rows added
                rows_added += len(rows_new)
            # If there is an error in fetching data, return a broken response
            except Exception as e:
                return [cur._gen_broken(msg=str(e),
                                        anchor=anchor)]
        # Return the list of rows
        return rows
        
    @staticmethod
    def _get_info(response: ResponseAPI,
                  name_list: str) -> tuple[list[dict[str, Any]], bool, int]:
        """
        ========================================================================
         Get the info from the data.
        ========================================================================
        """
        data = response.data['data']
        has_more = data['hasMore']
        cursor = data['cursor']
        return data[name_list], has_more, cursor

    @staticmethod
    def _gen_not_ok(status_code: int,
                    anchor: tuple[str, str]) -> dict[str, Any]:
        """
        ========================================================================
         Generate a not ok response.
        ========================================================================
        """
        return {'status_code': status_code,
                'is_ok': False,
                anchor[0]: anchor[1]}
    
    @staticmethod
    def _gen_not_found(anchor: tuple[str, str]) -> dict[str, Any]:
        """
        ========================================================================
         Generate a not found response.
        ========================================================================
        """ 
        return {'status_code': 404,
                'is_ok': True,
                'is_found': False,
                anchor[0]: anchor[1]}
    
    @staticmethod
    def _gen_broken(msg: str,
                    anchor: tuple[str, str]) -> dict[str, Any]:
        """
        ========================================================================
         Generate a broken response.
        ========================================================================
        """
        return {'is_ok': True,
                'is_found': True,
                'is_broken': True,
                'msg': msg,
                anchor[0]: anchor[1]}



    """
    @staticmethod
    def _fetch_multi(url: str,
                     params: dict[str, Any],
                     type_data: Type[DataAudit],
                     type_list: Type[DataList]) -> list[dict[str, Any]]:
        has_more = True
        cursor = 0
        rows_added = 1
        rows: list[dict[str, Any]] = list()
        gen = type_data.Gen
        while has_more and rows_added:
            rows_added = 0
            params['cursor'] = cursor
            response: ResponseAPI = RequestGet.get(url=url,
                                                   params=params,
                                                   headers=TiktokAPI._HEADERS)
            # Check if the response is ok.
            if not response:
                return [gen.not_ok(status_code=response.status,
                                   params=params)]
            # Check if the user is found.
            if not response.is_found:
                return [gen.not_found(params=params)]
            # Try fill the data.
            try:
                print('try')
                print(type(type_list))
                model = type_list()
                print('model')
                model = model.model_validate(response.data)
                rows_new = model.to_list()
                rows.extend(rows_new)
                rows_added += len(rows_new)
                has_more = model.has_more
                cursor = model.cursor
            except Exception as e:
                print(e)
                return [gen.broken(msg=str(e), params=params)]
        return rows
    """

    @staticmethod
    def old_videos_by_user(id_user: str) -> list[dict[str, Any]]:
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
