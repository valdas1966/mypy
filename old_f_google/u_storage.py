from google.cloud import storage
from tenacity import retry, stop_after_attempt, wait_random_exponential
from f_utils import u_file


@retry(stop=stop_after_attempt(5),
       wait=wait_random_exponential(multiplier=1, max=10))
def upload(json_key: str,
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


def upload_dag(path_dag: str) -> None:
    json_key = 'd:\\noteret\\repo\\viewer.json'
    project = 'gfunc-377012'
    str_bucket = 'us-central1-noteret-bf653c49-bucket'
    path_src = path_dag
    filename = path_dag.split('\\')[-1]
    path_dest = f'dags/{filename}'
    upload(json_key=json_key,
           project=project,
           str_bucket=str_bucket,
           path_src=path_src,
           path_dest=path_dest)


"""
json_key = 'd:\\noteret\\repo\\viewer.json'
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
