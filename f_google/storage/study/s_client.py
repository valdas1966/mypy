from f_google.storage.client import Client


path_json = 'd:\\professor\\json\\viewer.json'
client = Client(path_json=path_json)
for b in client.names_bucket():
    print(b)
    