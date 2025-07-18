# Google Cloud Storage Bucket

## Overview
Wrapper for Google Cloud Storage bucket operations with blob management and file uploads.

## Usage

### Get Bucket
```python
from f_google.services.storage import Storage

storage = Storage.Factory.rami()
bucket = storage.get_bucket('noteret_mp4')
```

### List Blobs
```python
# List all blobs
blobs = bucket.names_blobs()
print(f"Found {len(blobs)} blobs")

# List with prefix
videos = bucket.names_blobs(prefix='videos/')
```

### Get Blob
```python
blob = bucket.get_blob('videos/sample.mp4')
if blob:
    print(f"Found: {blob.name}")
```

### Upload from PC
```python
# Upload local file
success = bucket.upload_from_pc(
    name='data/report.pdf',           # destination in bucket
    path='/local/path/report.pdf'     # local file
)
print(f"Upload: {success}")
```

### Upload from URL
```python
# Upload from URL
success = bucket.upload_from_url(
    name='downloads/image.jpg',
    url='https://example.com/image.jpg'
)
print(f"URL upload: {success}")
```

### Delete Blob
```python
success = bucket.delete_blob('old/file.txt')
print(f"Deleted: {success}")
```

## API Reference

| Method | Returns | Description |
|--------|---------|-------------|
| `names_blobs(prefix=None)` | `list[str]` | List blob names |
| `get_blob(name)` | `Blob` or `None` | Get blob by name |
| `upload_from_pc(name, path)` | `bool` | Upload local file |
| `upload_from_url(name, url)` | `bool` | Upload from URL |
| `delete_blob(name)` | `bool` | Delete blob |

### Properties
| Property | Type | Description |
|----------|------|-------------|
| `name` | `str` | Bucket name |

## Notes
- Large files (>100MB) are automatically streamed for URL uploads
- Upload methods return `True` on success, `False` on failure
- Use prefixes to organize blobs like folders: `folder/subfolder/file.txt`