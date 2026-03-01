# Google Cloud Storage

## Overview
Wrapper for Google Cloud Storage operations with bucket management.

## Usage

### Basic Setup
```python
from f_google.services.storage import Storage

# Create storage instance
storage = Storage.Factory.rami()
```

### List Buckets
```python
# Get all bucket names
buckets = storage.names_buckets()
print(buckets)  # ['noteret_mp4', 'my-bucket', ...]
```

### Get Bucket
```python
# Get existing bucket
bucket = storage.get_bucket('noteret_mp4')
if bucket:
    print(f"Found: {bucket.name}")
```

### Create Bucket
```python
# Create new bucket (name must be globally unique)
import uuid
name = f'my-project-{uuid.uuid4().hex[:8]}'
bucket = storage.create_bucket(name)
```

### Delete Bucket
```python
# Delete bucket (must be empty)
success = storage.delete_bucket('old-bucket')
print(f"Deleted: {success}")
```

## API Reference

| Method | Returns | Description |
|--------|---------|-------------|
| `names_buckets()` | `list[str]` | List all bucket names |
| `get_bucket(name)` | `Bucket` or `None` | Get bucket by name |
| `create_bucket(name)` | `Bucket` | Create new bucket |
| `delete_bucket(name)` | `bool` | Delete bucket |

### Factory Methods
| Method | Returns |
|--------|---------|
| `Storage.Factory.rami()` | `Storage` |

## Notes
- Bucket names must be globally unique across all Google Cloud users
- Delete only works on empty buckets
- Use factory method for authentication