from old_f_google.services.big_query.client import BigQuery
from f_google.services.storage import Storage
from datetime import datetime
import time


tname_todo = 'noteret.tiktok.download_todo'
tname_done = 'noteret.tiktok.download_done'

bq = BigQuery()
df = bq.select.df(query=tname_todo)

rows = list()

storage = Storage.Factory.rami()
bucket = storage.get_bucket('noteret_mp4')

for index, row in df.iterrows():
    start = time.time() 
    id_video = row['id_video']
    play = row['play']
    name = f'{id_video}.mp4'
    blob = bucket.upload_from_url(name=name, url=play)
    size = blob.size if blob else 0
    finish = time.time()
    elapsed = round(finish - start)
    # STR-Format without microseconds
    str_start = datetime.now().isoformat()
    # Only HH:MI:SS
    time_start = str_start.split('.')[0].split('T')[1]
    print(f'{index}: {time_start} {id_video} [{size} mb] [{elapsed} secs]')
    d = {'id_video': id_video,
         'size': size,
         'elapsed': elapsed,
         'inserted': str_start}
    rows.append(d)
    if len(rows) % 1000 == 0:
        bq.insert.rows(tname=tname_done, rows=rows)
        rows = list()

if rows:
    bq.insert.rows(tname=tname_done, rows=rows)
        
storage.close()
