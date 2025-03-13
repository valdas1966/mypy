from f_proj.rapid_api.c_tiktok import TikTok


id_user = '107955'
count = 0
has_more = True
time = 0
t = TikTok()
while has_more:
    followers, has_more, time = t.user.followers(id_user=id_user, time=time)
    count += 1
    if count == 3:
        break
