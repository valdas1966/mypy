from proj.rapid_api.c_tiktok import TikTok


user_valid = '107955'
user_invalid = '12345'

t = TikTok()

print(t.user.info(id_user=user_valid))
print(t.user.info(id_user=user_invalid))
