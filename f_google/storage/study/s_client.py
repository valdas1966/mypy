from f_google.storage.client import Storage


storage = Storage(user='GFUNC')
for b in storage.names_bucket():
    print(b)
    