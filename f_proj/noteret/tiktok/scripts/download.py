from old_f_google.services.big_query.client import BigQuery
from f_google.services.storage import Storage
import time


tname = 'noteret.tiktok.download_todo'

bq = BigQuery()
df = bq.select.df(query=tname)

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
    elapsed = finish - start
    start_str = time.strftime('%H:%M:%S', time.gmtime(start))
    print(f'{start_str} {id_video} [{size} mg] [{elapsed} secs]')
        
storage.close()
