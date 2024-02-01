from google.cloud import storage
from f_google.utils import u_auth


path_json = 'd:\\professor\\json\\viewer.json'
creds = u_auth.get_credentials(path_json=path_json)
client = storage.Client(credentials=creds)
print(type(client))

for bucket in client.list_buckets():
    print(type(bucket))
    print(bucket.name)
