from f_google.big_query.client import Client


client = Client(user='RAMI')

print(client.creds.project_id)
print(type(client._client))
