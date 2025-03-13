from f_proj.rapid_api.c_tiktok import TikTok


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
    print(d.keys())
    print(d['code'])
    print(d['msg'])
    print(d['data'].keys())
    print(d['data']['followers'][0].keys())
    print(d['data']['followers'][0]['unique_id'])
    print(d['data']['followers'][0]['nickname'])
    print(len(d['data']['followers']))



id_user = '107955'
# id_user = '111'
# s_videos_by_hashtag()
# get_tiktok_info()
get_followers(id_user=id_user)
