from f_google import u_storage


def upload():
     json_key = 'd:\\noteret\\repo\\viewer.json'
     project = 'noteret'
     project = 'gfunc-377012'
     path_src = 'd:\\temp\\sp500.xlsx'
     subfolder = 'dags/'
     path_dest = f'{subfolder}test.json'
     str_bucket = 'json_tiktok_by_hashtag'
     str_bucket = 'us-central1-noteret-bf653c49-bucket'
     # str_bucket = 'dag_test'
     u_storage.upload(json_key=json_key,
          project=project,
          str_bucket=str_bucket,
          path_src=path_src,
          path_dest=path_dest)


def upload_dag():
     path_dag = 'd:\\temp\\2023\\04\\study_tiktok_by_hashtag.py'
     u_storage.upload_dag(path_dag)


upload_dag()
