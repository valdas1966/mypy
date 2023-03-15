from f_rapid_api.c_tiktok import TikTok
from f_utils import u_file


path_key = 'd:\\professor\\gcp\\tiktok no watermark.txt'
key = u_file.read(path_key)

t = TikTok(key=key)
url = t.id_video_to_url(id_video='7106658991907802411')
print(type(url), url)

