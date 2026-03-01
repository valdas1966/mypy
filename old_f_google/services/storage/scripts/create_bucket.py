from old_f_google.services.storage import Storage


storage = Storage()
name = 'tiktok_downloads'
bucket = storage.create_bucket(name=name)
if bucket:
    print(f"Bucket '{bucket.name}' created successfully.")
else:
    print(f'Failed to create bucket {name}.')
storage.close()
