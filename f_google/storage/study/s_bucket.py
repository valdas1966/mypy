from f_google.storage.client import Storage
from f_google.storage.bucket import Bucket


storage = Storage(user='GFUNC')
bucket: Bucket = storage.bucket(name='us-central1-noteret-bf653c49-bucket')
folders = bucket.folders(folder='plugins/')
print(folders)
files = bucket.files(folder='plugins/')
print(files)


"""
bucket.upload_file(path_from='d:\\temp\\2023\\02\\select.py',
                   path_to='plugins/select.py')
print(bucket.files(folder='plugins/'))
"""