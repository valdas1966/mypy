from f_google.services.storage import Storage


storage = Storage.Factory.rami()
for bucket in storage.names_buckets():
    print(bucket)
