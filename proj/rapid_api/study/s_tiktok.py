from proj.rapid_api.c_tiktok import TikTok


# path_key = 'd:\\professor\\gcp\\tiktok no watermark.old_old_txt'
# key = u_file.read(path_key)


def s_id_video_to_url():
    t = TikTok()
    url = t.id_video_to_url(id_video='7106658991907802411')
    print(type(url), url)


def s_videos_by_hashtag():
    t = TikTok()
    r = t.videos_by_hashtag('13864220')
    print(r)


def get_tiktok_info():
    t = TikTok()
    id_user = t.alias_to_id(alias='therock')
    print(id_user)


def get_followers(id_user: str, time: str = str()):
    d = TikTok().get_followers(id_user=id_user, time=time)
    print(d['msg'])
    print(d)


id_user = '107955'
# s_videos_by_hashtag()
# get_tiktok_info()
get_followers(id_user=id_user)
