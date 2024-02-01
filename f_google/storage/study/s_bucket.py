from f_google.storage.client import Client
from f_google.storage.bucket import Bucket

path_json = 'd:\\professor\\json\\viewer.json'
client = Client(path_json=path_json)
bucket = client.bucket(name='noteret_json')
print(bucket.folders())
