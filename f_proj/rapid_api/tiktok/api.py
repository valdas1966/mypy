from f_os import u_environ
from f_proj.rapid_api.tiktok.data.i_1_user_snapshot import DataUserSnapshot
from f_proj.rapid_api.tiktok.data.i_1_videos_from_music import DataVideosFromMusic
from f_proj.rapid_api.tiktok.data.i_1_videos_from_hashtag import DataVideosFromHashtag
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
            params = {'music_id': id_music, 'count': 35, 'cursor': cursor}
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

    @staticmethod
    def videos_from_hashtag(id_hashtag: str) -> list[dict]:
        """
        ============================================================================
         Get videos from hashtag.
        ============================================================================
        """
        rows: list[dict] = list()
        has_more = True
        cursor = 0
        url = f'https://{TiktokAPI._HOST}/challenge/posts'
        rows_added = 1
        while has_more and rows_added:
            rows_added = 0
            params = {'challenge_id': id_hashtag,
                      'count': 20,
                      'cursor': cursor}
            _input = Input(url=url, params=params, headers=TiktokAPI._HEADERS)
            output = RequestGet(_input=_input).run()
            if output:
                try:
                    d = output.to_dict()['data']
                except KeyError:
                    return [DataVideosFromHashtag(id_hashtag=id_hashtag,
                                                  is_ok=True,
                                                  is_found=False).to_dict()]
                has_more = bool(d['hasMore'])
                cursor = d['cursor']
                for d_video in d['videos']:
                    data = DataVideosFromHashtag()
                    data.id_hashtag = id_hashtag
                    data.is_ok = True
                    data.is_found = True
                    data.id_video = d_video['video_id']
                    data.id_user = d_video['author']['id']
                    data.id_user_unique = d_video['author']['unique_id']
                    data.nick = d_video['author']['nickname']
                    data.region = d_video['region']
                    data.title = d_video['title']
                    data.created = d_video['create_time']
                    data.duration = d_video['duration']
                    data.plays = d_video['play_count']
                    data.shares = d_video['share_count']
                    data.diggs = d_video['digg_count']
                    data.downloads = d_video['download_count']
                    data.comments = d_video['comment_count']
                    data.is_ad = str(d_video['is_ad'])
                    rows.append(data.to_dict())
                    len_rows = len(rows)
                    if len_rows % 100 == 0:
                        print(f'Cached {len_rows} rows so far')
                    if len(rows) >= 1000000:
                        return rows
                    rows_added += 1
            elif output.reason == Reasons.NOT_FOUND:
                return [DataVideosFromHashtag(id_hashtag=id_hashtag,
                                              is_ok=True,
                                              is_found=False).to_dict()]
            else:
                return [DataVideosFromHashtag(id_hashtag=id_hashtag,
                                              is_ok=False,
                                              is_found=False).to_dict()]
        return rows
            
