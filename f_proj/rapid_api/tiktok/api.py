from f_os import u_environ
from f_proj.rapid_api.tiktok.data.i_1_user_snapshot import DataUserSnapshot
from f_proj.rapid_api.tiktok.data.i_1_videos_from_music import DataVideosFromMusic
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
        output = RequestGet(_input=_input).run()
        data = DataUserSnapshot()
        if output:
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
        elif output.reason == Reasons.NOT_FOUND:
            data.is_ok = True
            data.is_found = False
        else:
            data.is_ok = False
        return data

    @staticmethod
    def videos_from_music(id_music: str) -> list[dict]:
        rows: list[dict] = list()
        has_more = True
        cursor = 0
        url = f'https://{TiktokAPI._HOST}/music/posts'
        rows_added = 1
        while has_more and rows_added:
            rows_added = 0
            params = {'music_id': id_music, 'count': 35, cursor: cursor}
            _input = Input(url=url, params=params, headers=TiktokAPI._HEADERS)
            output = RequestGet(_input=_input).run()
            if output:
                try:
                    d = output.to_dict()['data']
                except KeyError:
                    return [DataVideosFromMusic(id_music=id_music,
                                                is_ok=True,
                                                is_found=False).to_dict()]
                has_more = bool(d['hasMore'])
                cursor = d['cursor']
                for d_video in d['videos']:
                    data = DataVideosFromMusic()
                    data.id_music = id_music
                    data.is_ok = True
                    data.is_found = True
                    data.id_video = d_video['video_id']
                    data.id_user = d_video['author']['id']
                    rows.append(data.to_dict())
                    if len(rows) >= 10000:
                        return rows
            elif output.reason == Reasons.NOT_FOUND:
                return [DataVideosFromMusic(id_music=id_music,
                                            is_ok=True,
                                            is_found=False).to_dict()]
            else:
                return [DataVideosFromMusic(id_music=id_music,
                                            is_ok=False,
                                            is_found=False).to_dict()]
        return rows

