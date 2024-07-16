from f_google.storage.client import Storage
from f_google.storage.bucket import Bucket


def study_1():
    storage = Storage(user='GFUNC')
    bucket: Bucket = storage.bucket(name='us-central1-noteret-bf653c49-bucket')
    folders = bucket.folders(folder='plugins/')
    print(folders)
    files = bucket.files(folder='plugins/')
    print(files)


def study_2():
    pass
    """
    bucket.upload_file(path_from='d:\\temp\\2023\\02\\select.py',
                       path_to='plugins/select.py')
    print(bucket.files(folder='plugins/'))
    """


def upload_file():
    storage = Storage(user='RAMI')
    bucket = storage.bucket(name='json_tiktok_by_music')
    folders = bucket.folders()
    print(f'folders: {folders}')
    files = bucket.files()
    print(f'files: {files}')
    path = 'd:\\mypy\\proj\\rapid_api\\study\\7314259878682446594_20240715081606.json'
    bucket.upload_file(path_from=path)
    folders = bucket.folders()
    print(f'folders: {folders}')
    files = bucket.files()
    print(f'files: {files}')


upload_file()
