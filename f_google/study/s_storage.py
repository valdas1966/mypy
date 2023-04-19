from f_google import u_storage


json_key = 'd:\\tiktok\\repo\\viewer.json'
project = 'noteret'
project = 'gfunc-377012'
path_src = 'd:\\temp\\temp.json'
path_dest = 'test.json'
str_bucket = 'json_tiktok_by_hashtag'
str_bucket = 'us-central1-noteret-bf653c49-bucket/dags'
# str_bucket = 'dag_test'
u_storage.upload(json_key=json_key,
     project=project,
     str_bucket=str_bucket,
     path_src=path_src,
     path_dest=path_dest)
