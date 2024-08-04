from proj.rapid_api.c_tiktok import TikTok
from f_utils import u_datetime
from f_file.c_json import Json
from f_google.storage.client import Storage
from f_os.u_file import UFile as u_file
import os


id_music = '7318314841177508614'


t = TikTok()
videos = t.music.get_videos(id_music)
storage = Storage(user='RAMI')
bucket = storage.bucket(name='json_tiktok_by_music')
while videos and videos.has_more:
    path = f'{os.getcwd()}\\{id_music}_{u_datetime.now(format='NUM')}.json'
    f = Json.from_data(path=path, data=videos.json)
    bucket.upload_file(path_from=path)
    u_file.delete(path=path)
    print(f, len(videos.videos), 'videos')
    videos = t.music.get_videos(id_music=id_music, cursor=videos.cursor)
