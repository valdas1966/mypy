from f_proj.rapid_api.c_tiktok import TikTok
from f_utils import u_datetime
from f_file_old.c_json import Json
from f_google.services.storage.client import Storage
from f_os.u_file import UFile as u_file
import os


id_music = '7314259878682446594'


t = TikTok()
videos = t.music.get_videos(id_music)
storage = Storage(user='RAMI')
bucket = storage.bucket(name='json_tiktok_by_music')
while videos:
    path = f'{os.getcwd()}\\{id_music}_{u_datetime.now(format="NUM")}.json'
    f = Json.from_data(path=path, data=videos.json)
    bucket.upload_file(path_from=path)
    u_file.delete(path=path)
    print(f, len(videos.videos), 'videos')
    videos = t.music.get_videos(id_music=id_music, cursor=videos.cursor)
    if not videos.has_more:
        break
