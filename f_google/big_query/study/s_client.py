from f_google.big_query.client import Client


client = Client(user='RAMI')

print(type(client._client))
