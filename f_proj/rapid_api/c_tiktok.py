from __future__ import annotations
from collections import namedtuple
from f_proj.rapid_api.requests.tiktok.user import User
from f_proj.rapid_api.requests.tiktok.music import Music
from f_utils import u_http_requests
from f_os import u_environ


class TikTok:
    """
    ============================================================================
     1. TikTok-Crawler - Tiktok video no watermark.
     2. https://rapidapi.com/yi005/api/tiktok-video-no-watermark2/
    ============================================================================
    """

    #_PATH_KEY = 'd:\\professor\\json\\tiktok no watermark.txt'

    def __init__(self) -> None:
        """
        ========================================================================
         Init private Attributes.
        ========================================================================
        """
        self._host = 'tiktok-video-no-watermark2.p.rapidapi.com'
        self._key = u_environ.get('TIKTOK_1')
        self._headers: dict[str, str] = {'X-RapidAPI-Host': self._host,
                                         'X-RapidAPI-Key': self._key,
                                         }
        self.user = User(self._key, self._host, self._headers)
        self.music = Music(self._key, self._host, self._headers)

    def id_video_to_url(self, id_video: str) -> str:
        """
        ========================================================================
         1. Get Id-Video (str).
         2. Return URL to play / download the Video (str).
        ========================================================================
        """
        url = f'https://{self._host}/'
        params = {'url': f'https://www.tiktok.com/@tiktok/video/{id_video}',
                  'hd': '0'}
        d = u_http_requests.get_dict(url=url,
                                     params=params,
                                     headers=self._headers)
        return d['data']['play']
    
    def videos_by_hashtag(self,
                          hashtag_id: str,
                          cursor: int = 0) -> dict:
        """
        ========================================================================
         1. Get Id-Hashtag (str) and Cursor (int).
         2. Return next 100 Videos with this Hashtag.
        ========================================================================
        """
        url = f'https://{self._host}/challenge/posts'
        params = {'challenge_id': hashtag_id,
                  'count': '100',
                  'cursor': cursor}
        return u_http_requests.get_dict(url=url,
                                        params=params,
                                        headers=self._headers)

    def alias_to_id(self, alias: str) -> str:
        """
        ========================================================================
         1. Get User's Alias (str).
         2. Return User's Id (str).
        ========================================================================
        """
        url = f'https://{self._host}/user/info'
        params = {'unique_id': alias}
        r = u_http_requests.get_dict(url=url,
                                     params=params,
                                     headers=self._headers)
        try:
            return r['data']['user']['id']
        except Exception:
            return alias

    def keyword_to_hashtags(self, keyword: str) -> tuple[namedtuple, ...]:
        """
        ========================================================================
         Return Top-10 Hashtags associated to the given Keyword.
        ========================================================================
        """
        url: str = f'https://{self._host}/challenge/search'
        params: dict[str, str] = {'keywords': keyword,
                                  'count': '10',
                                  'cursor': "0"}
        r = u_http_requests.get_dict(url=url,
                                     params=params,
                                     headers=self._headers)
        try:
            results: list[dict[str, str|int]] = r['data']['challenge_list']
            Hashtag = namedtuple('Hashtag',
                                 ['id', 'name', 'users'])
            return tuple(Hashtag(id=d['id'],
                                 name=d['cha_name'],
                                 users=d['user_count'])
                         for d in results)
        except Exception as e:
            print(e)

    def get_followers(self,
                      id_user: str,
                      time: str = str()) -> dict:
        """
        ========================================================================
         Return 200 Followers of the given User.
        ========================================================================
        """
        url = f'https://{self._host}/user/followers'
        params: dict[str, str] = {'user_id': id_user,
                                  'count': '200',
                                  'time': time}
        r = u_http_requests.get_dict(url=url,
                                     params=params,
                                     headers=self._headers)
        return r

