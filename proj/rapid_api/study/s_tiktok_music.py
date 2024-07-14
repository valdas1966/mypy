from proj.rapid_api.c_tiktok import TikTok
from f_utils import u_datetime
from f_file.c_json import Json
import os


id_music = '7002634556977908485'


t = TikTok()
videos = t.music.get_videos(id_music)
while videos and videos.has_more:
    path = f'{os.getcwd()}\\{id_music}_{u_datetime.now(format='NUM')}.json'
    f = Json.from_data(path=path, data=videos.videos)
    print(f, len(videos.videos), 'videos')
    videos = t.music.get_videos(id_music=id_music, cursor=videos.cursor)
