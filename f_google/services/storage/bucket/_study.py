from f_google.services.storage import Storage, Bucket


storage: Storage = Storage.Factory.rami()
bucket: Bucket = storage.bucket('noteret_mp4')
print(len(bucket.blobs()))
