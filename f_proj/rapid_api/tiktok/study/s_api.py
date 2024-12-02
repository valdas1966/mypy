from f_proj.rapid_api.tiktok.api import TiktokAPI

data = TiktokAPI.user_snapshot(id_user='107955')
print(data)
print(data.is_ok, data.is_found, data.nick)

print()

data = TiktokAPI.user_snapshot(id_user='12345')
print(data)
print(data.is_ok, data.is_found, data.nick)
