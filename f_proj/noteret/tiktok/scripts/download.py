from old_old_f_google.services.big_query.client import BigQuery
from old_f_google.services.storage import Storage
from datetime import datetime
from f_http.url import URL
import time


tname_todo = 'noteret.tiktok.download_todo'

bq = BigQuery()
df = bq.select.df(query=tname_todo)

storage = Storage.Factory.rami()
bucket = storage.get_bucket('tiktok_downloads')

for index, row in df.iterrows():
    start = time.time() 
    id = row['id']
    url = row['url']
    name = f'{id}.{URL(url=url).suffix()}'
    blob = bucket.upload_from_url(name=name, url=url)
    size = blob.size if blob else 0
    finish = time.time()
    elapsed = round(finish - start)
    # STR-Format without microseconds
    str_start = datetime.now().isoformat()
    # Only HH:MI:SS
    time_start = str_start.split('.')[0].split('T')[1]
    print(f'{index}: {time_start} {name} [{size} mb] [{elapsed} secs]')

storage.close()
