from f_rapid_api.c_tiktok import TikTok
from f_utils import u_file


path_key = 'd:\\professor\\gcp\\tiktok no watermark.old_old_txt'
key = u_file.read(path_key)


def s_id_video_to_url():
    t = TikTok(key=key)
    url = t.id_video_to_url(id_video='7106658991907802411')
    print(type(url), url)


def s_videos_by_hashtag():
    t = TikTok(key=key)
    r = t.videos_by_hashtag('13864220')
    print(r)


def get_tiktok_info():
    t = TikTok(key=key)
    id_user = t.alias_to_id(alias='therock')
    print(id_user)


# s_videos_by_hashtag()

get_tiktok_info()
