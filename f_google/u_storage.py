from google.cloud import storage
from f_logging.dec import log_info

json_key = 'd:\\professor\\gcp\\storage.json'
project = 'crafty-stock-253813'


@log_info
def copy(str_bucket: str,
         path_src: str,
         path_dest: str):
    client = storage.Client.from_service_account_json(json_key, project=project)
    bucket = client.bucket(str_bucket)
    blob = bucket.blob(path_dest)
    blob.upload_from_filename(path_src)
    if not storage.Blob(bucket=bucket, name=path_dest):
        raise Exception(f'{path_dest} is not found on Google Storage')


"""
path_src = 'd:\\professor\\repo\\mp4\\7075396968930954497.mp4'
path_dest = 'mp4/7075396968930954497.mp4'
str_bucket = 'tiktok_movies'
copy(str_bucket, path_src, path_dest)
"""
