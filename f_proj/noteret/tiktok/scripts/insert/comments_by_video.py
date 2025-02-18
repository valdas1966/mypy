from f_google.services.big_query.client import BigQuery
from f_proj.rapid_api.tiktok.api import TiktokAPI
from f_proj.noteret.tiktok.tables import Tables
from f_utils import u_datetime


def prod():
    bq = BigQuery()
    videos = bq.select.list(Tables.COMMENTS_BY_VIDEO_TODO)
    for i, id_video in enumerate(videos):
        print(f'{u_datetime.now()} Start working on video: [{id_video}] '
              f'[{i+1} / {len(videos)}]')
        tname = Tables.COMMENTS_BY_VIDEO
        rows = TiktokAPI.comments_from_videos(id_video=id_video)
        if rows:
            try:
                bq.insert.rows_inserted(tname=tname, rows=rows)
            except Exception as e:
                print(str(e))
        else:
            print(u_datetime.now(), len(rows), f'[{i + 1} / {len(videos)}]')


prod()
