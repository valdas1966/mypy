from f_utils import u_http_requests


class TikTok:

    def __init__(self, key: str):
        self._host = 'tiktok-video-no-watermark2.p.rapidapi.com'
        self._key = key
        self._headers = {'X-RapidAPI-Key': self._key,
                         'X-RapidAPI-Host': self._host}

    def id_video_to_url(self, id_video: str) -> str:
        url = f'https://{self._host}/'
        params = {'url': f'https://www.tiktok.com/@tiktok/video/{id_video}',
                  'hd': '0'}
        d = u_http_requests.get_dict(url=url,
                                     params=params,
                                     headers=self._headers)
        return d['data']['play']
