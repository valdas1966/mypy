from google.cloud import storage
from tenacity import retry, stop_after_attempt


@retry(stop=stop_after_attempt(5))
def copy(json_key: str,
         project: str,
         str_bucket: str,
         path_src: str,
         path_dest: str):
    client = storage.Client.from_service_account_json(json_key, project=project)
    bucket = client.bucket(str_bucket)
    blob = bucket.blob(path_dest)
    blob.upload_from_filename(path_src)
    if not storage.Blob(bucket=bucket, name=path_dest):
        raise Exception(f'{path_dest} is not found on Google Storage')

"""
json_key = 'd:\\tiktok\\repo\\viewer.json'
project = 'noteret'
path_src = 'd:\\professor\\repo\\mp4\\7075396968930954497.mp4'
path_dest = '7075396968930954497.mp4'
str_bucket = 'noteret_mp4'
copy(json_key=json_key,
     project=project,
     str_bucket=str_bucket,
     path_src=path_src,
     path_dest=path_dest)
"""
