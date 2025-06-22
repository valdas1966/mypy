from f_proj.rapid_api.tiktok.api.api import TiktokAPI
from typing import Any


class RequestsTiktok:
    """
    ============================================================================
     Class for requests to TikTok-API on Rapid-API.
    ============================================================================
    """

    @staticmethod
    def users_by_id(id_user: str) -> dict[str, Any]:
        """
        ========================================================================
         Fetch users by their ids.
        ========================================================================
        """
        url = f'https://{TiktokAPI._HOST}/user/info'
        params = {'user_id': id_user}

        def to_row(item: dict[str, Any]) -> dict[str, Any]:
            row: dict[str, Any] = dict()
            row['id_user_unique'] = item['user']['uniqueId']
            row['id_user'] = item['user']['id']
            row['nick'] = item['user']['nickname']
            row['is_verified'] = item['user']['verified']
            row['is_secret'] = item['user']['secret']
            row['is_private'] = item['user']['privateAccount']
            row['videos'] = item['stats']['videoCount']
            row['hearts'] = item['stats']['heartCount']
            row['diggs'] = item['stats']['diggCount']
            row['followers'] = item['stats']['followerCount']
            row['following'] = item['stats']['followingCount']
            row['is_ok'] = True
            row['is_broken'] = False
            return row

        return TiktokAPI.fetch_single(url=url,
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
            row['id_user'] = data['user']['id']
            row['nick'] = data['user']['nickname']
            row['is_verified'] = data['user']['verified']
            row['is_secret'] = data['user']['secret']
            row['is_private'] = data['user']['privateAccount']
            row['videos'] = data['stats']['videoCount']
            row['hearts'] = data['stats']['heartCount']
            row['diggs'] = data['stats']['diggCount']
            row['followers'] = data['stats']['followerCount']
            row['following'] = data['stats']['followingCount']
            row['is_ok'] = True
            row['is_found'] = True
            row['is_broken'] = False
            return row

        return TiktokAPI.fetch_single(url=url,
                                      params=params,
                                      anchor=('id_user_unique', id_user_unique),
                                      to_row=to_row)

    @staticmethod
    def videos_by_user(id_user: str, limit: int = None) -> list[dict[str, Any]]:
        """
        ========================================================================
         Fetch videos by user id.
        ========================================================================
        """
        url = f'https://{TiktokAPI._HOST}/user/posts'
        params = {'user_id': id_user, 'count': 50,
                  'cursor': '0', 'id_user': id_user}

        def to_rows(items: list[dict[str, Any]]) -> list[dict[str, Any]]:
            rows: list[dict[str, Any]] = list()
            for item in items:
                row: dict[str, Any] = dict()
                row['id_user'] = id_user
                row['id_music'] = item['music_info']['id']
                row['id_video'] = item['video_id']
                row['region'] = str(item['region'])
                row['title'] = item['title']
                row['created'] = item['create_time']
                row['duration'] = item['duration']
                row['plays'] = item['play_count']
                row['shares'] = item['share_count']
                row['diggs'] = item['digg_count']
                row['comments'] = item['comment_count']
                row['downloads'] = item['download_count']
                row['is_ad'] = item['is_ad']
                row['play'] = item['play']
                row['is_ok'] = True
                row['is_found'] = True
                row['is_broken'] = False
                rows.append(row)
            return rows

        return TiktokAPI.fetch_multi(url=url,
                                      params=params,
                                      anchor=('id_user', id_user),
                                      name_list='videos',
                                      to_rows=to_rows,
                                      limit=limit)

    @staticmethod
    def videos_new_by_user(# Id_User to crawl
                           id_user: str,
                           # Last created time (crawl only after this time)
                           created: str) -> list[dict[str, Any]]:
        """
        ========================================================================
         Fetch videos by user id (crawl only after this time).
        ========================================================================
        """
        url = f'https://{TiktokAPI._HOST}/user/posts'
        params = {'user_id': id_user, 'count': 50,
                  'cursor': 0, 'id_user': id_user}

        def to_rows(items: list[dict[str, Any]]) -> list[dict[str, Any]]:
            rows: list[dict[str, Any]] = list()
            for item in items:
                row: dict[str, Any] = dict()
                row['id_user'] = id_user
                row['id_music'] = item['music_info']['id']
                row['id_video'] = item['video_id']
                row['region'] = str(item['region'])
                row['title'] = item['title']
                row['created'] = item['create_time']
                row['duration'] = item['duration']
                row['plays'] = item['play_count']
                row['shares'] = item['share_count']
                row['diggs'] = item['digg_count']
                row['comments'] = item['comment_count']
                row['downloads'] = item['download_count']
                row['is_ad'] = item['is_ad']
                row['play'] = item['play']
                row['is_ok'] = True
                row['is_broken'] = False
                # If the video was created after the last created time,
                #  add it to the list. Otherwise, return the list.
                if created != '<NA>' and row['created'] <= created:
                    break
                # Add the row to the list
                rows.append(row)
            return rows

        return TiktokAPI.fetch_multi(url=url,
                                      params=params,
                                      anchor=('id_user', id_user),
                                      name_list='videos',
                                      to_rows=to_rows)

    @staticmethod
    def hashtags_by_keyword(keyword: str, limit: int = None) -> list[dict[str, Any]]:
        """
        ========================================================================
         Fetch hashtags by keyword.
        ========================================================================
        """
        url = f'https://{TiktokAPI._HOST}/challenge/search'
        params = {'keywords': keyword, 'count': 50, 'cursor': 0}

        def to_rows(items: list[dict[str, Any]]) -> list[dict[str, Any]]:
            rows: list[dict[str, Any]] = list()
            for item in items:
                row: dict[str, Any] = dict()
                row['keyword'] = keyword
                row['id_hashtag'] = item['id']
                row['hashtag'] = item['cha_name']
                row['users'] = item['user_count']
                row['views'] = item['view_count']
                row['is_ok'] = True
                row['is_broken'] = False
                rows.append(row)
            return rows

        return TiktokAPI.fetch_multi(url=url,
                                     params=params,
                                     anchor=('keyword', keyword),
                                     name_list='challenge_list',
                                     to_rows=to_rows,
                                     limit=limit)

    @staticmethod
    def videos_by_hashtag(id_hashtag: str,
                          limit: int = None) -> list[dict[str, Any]]:
        """
        ========================================================================
         Fetch videos by hashtag id.
        ========================================================================
        """
        url = f'https://{TiktokAPI._HOST}/challenge/posts'
        params = {'challenge_id': id_hashtag, 'count': 50, 'cursor': 0}

        def to_rows(items: list[dict[str, Any]]) -> list[dict[str, Any]]:
            rows: list[dict[str, Any]] = list()
            for item in items:
                row: dict[str, Any] = dict()
                row['id_hashtag'] = id_hashtag
                row['id_user'] = item['author']['id']
                row['id_user_unique'] = item['author']['unique_id']
                row['nick'] = item['author']['nickname']
                row['id_video'] = item['video_id']
                row['region'] = str(item['region'])
                row['title'] = item['title']
                row['created'] = item['create_time']
                row['duration'] = item['duration']
                row['plays'] = item['play_count']
                row['shares'] = item['share_count']
                row['diggs'] = item['digg_count']
                row['comments'] = item['comment_count']
                row['downloads'] = item['download_count']
                row['is_ad'] = item['is_ad']
                row['play'] = item['play']
                row['is_ok'] = True
                row['is_broken'] = False
                rows.append(row)
            return rows

        return TiktokAPI.fetch_multi(url=url,
                                     params=params,
                                     anchor=('id_hashtag', id_hashtag),
                                     name_list='videos',
                                     to_rows=to_rows,
                                     limit=limit)

    @staticmethod
    def followers_by_user(id_user: str, limit: int = None) -> list[dict[str, Any]]:
        """
        ========================================================================
         Fetch followers by user id.
        ========================================================================
        """
        url = f'https://{TiktokAPI._HOST}/user/followers'
        params = {'user_id': id_user, 'count': 50, 'time': 0}

        def to_rows(items: list[dict[str, Any]]) -> list[dict[str, Any]]:
            rows: list[dict[str, Any]] = list()
            for item in items:
                row: dict[str, Any] = dict()
                row['id_user'] = id_user
                row['id_follower'] = item['id']
                row['id_user_unique'] = item['unique_id']
                row['nick'] = item['nickname']
                row['region'] = item['region']
                row['is_verified'] = item['verified']
                row['is_secret'] = item['secret']
                row['followers'] = item['follower_count']
                row['following'] = item['following_count']
                row['aweme'] = item['aweme_count']
                row['favorited'] = item['total_favorited']
                row['is_ok'] = True
                row['is_broken'] = False
                rows.append(row)
            return rows

        return TiktokAPI.fetch_multi(url=url,
                                     params=params,
                                     anchor=('id_user', id_user),
                                     name_list='followers',
                                     name_cursor='time',
                                     to_rows=to_rows,
                                     limit=limit)

    @staticmethod
    def music_by_id(id_music: str) -> dict[str, Any]:
        """
        ========================================================================
         Fetch music by id.
        ========================================================================
        """
        url = f'https://{TiktokAPI._HOST}/music/info'
        params = {'url': id_music}

        def to_row(item: dict[str, Any]) -> dict[str, Any]:
            row: dict[str, Any] = dict()
            row['id_music'] = id_music
            row['title'] = item['title']
            row['play'] = item['play']
            row['author'] = item['author']
            row['duration'] = item['duration']
            row['is_original'] = item['original']
            row['videos'] = item['video_count']
            row['is_ok'] = True
            row['is_broken'] = False
            return row

        return TiktokAPI.fetch_single(url=url,
                                      params=params,
                                      anchor=('id_music', id_music),
                                      to_row=to_row)

    @staticmethod
    def videos_by_music(id_music: str, limit: int = None) -> dict[str, Any]:
        """
        ========================================================================
         Fetch videos by music id.
        ========================================================================
        """
        url = f'https://{TiktokAPI._HOST}/music/posts'
        params = {'music_id': id_music, 'count': 50, 'cursor': 0}

        def to_rows(items: list[dict[str, Any]]) -> list[dict[str, Any]]:
            rows: list[dict[str, Any]] = list()
            for item in items:
                row: dict[str, Any] = dict()
                row['id_music'] = id_music
                row['id_video'] = item['video_id']
                row['id_user'] = item['author']['id']
                row['is_ok'] = True
                row['is_broken'] = False
                rows.append(row)
            return rows

        return TiktokAPI.fetch_multi(url=url,
                                     params=params,
                                     anchor=('id_music', id_music),
                                     name_list='videos',
                                     to_rows=to_rows,
                                     limit=limit)

    @staticmethod
    def comments_by_video(id_video: str, limit: int = None) -> list[dict[str, Any]]:
        """
        ========================================================================
         Fetch comments by video id.
        ========================================================================
        """
        url = f'https://{TiktokAPI._HOST}/comment/list'
        params = {'url': f'https://www.tiktok.com/@tiktok/video/{id_video}',
                  'count': 50,
                  'cursor': 0}

        def to_rows(items: list[dict[str, Any]]) -> list[dict[str, Any]]:
            rows: list[dict[str, Any]] = list()
            for item in items:
                row: dict[str, Any] = dict()
                row['id_video'] = id_video
                row['id_comment'] = item['id']
                row['text'] = item['text']
                row['replies'] = item['reply_total']
                row['diggs'] = item['digg_count']
                row['created'] = item['create_time']
                row['id_user'] = item['user']['id']
                row['id_user_unique'] = item['user']['unique_id']
                row['nick'] = item['user']['nickname']
                row['region'] = item['user']['region']
                row['aweme'] = item['user']['aweme_count']
                row['favorited'] = item['user']['total_favorited']
                row['followers'] = item['user']['follower_count']
                row['following'] = item['user']['following_count']
                row['is_ok'] = True
                row['is_broken'] = False
                rows.append(row)
            return rows

        return TiktokAPI.fetch_multi(url=url,
                                     params=params,
                                     anchor=('id_video', id_video),
                                     name_list='comments',
                                     to_rows=to_rows,
                                     limit=limit)
