from f_proj.rapid_api.tiktok.api import TiktokAPI

data = TiktokAPI.user_snapshot(id_user='107955')
print(data.is_ok)
print(data.is_found)
print(data.nick)

data = TiktokAPI.user_snapshot(id_user='12345')
print(data.is_ok)
print(data.is_found)
print(data.nick)