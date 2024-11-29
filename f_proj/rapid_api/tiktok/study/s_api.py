from f_proj.rapid_api.tiktok.api import TiktokAPI

t = TiktokAPI.user_info(id_user='107955')

print(t.is_succeed)
print(t.is_found)
print(t.data.nick)