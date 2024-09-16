from proj.rapid_api.c_tiktok import TikTok


id_user = '107955'
t = TikTok()
followers = t.user.followers(id_user=id_user)

for i, f in enumerate(followers):
    print(i, f)
    if i == 10:
        break
