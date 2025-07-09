from f_google import Storage


storage = Storage.Factory.rami()
for name in storage.names_buckets():
    print(name)
