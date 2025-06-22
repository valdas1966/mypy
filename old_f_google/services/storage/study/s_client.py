from old_f_google.services.storage.client import Storage


# storage = Storage(user='GFUNC')
storage = Storage(user='RAMI')
for b in storage.names_bucket():
    print(b)
    