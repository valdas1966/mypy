# Google Cloud Storage Blob

## Overview
Lightweight wrapper for Google Cloud Storage blob with basic properties.

## Usage

### Get Blob
```python
# Get blob from bucket
blob = bucket.get_blob('videos/sample.mp4')
if blob:
    print(f"Name: {blob.name}")
    print(f"Size: {blob.size} MiB")
```

### Check File Sizes
```python
# Check multiple blob sizes
blob_names = bucket.names_blobs()
for name in blob_names:
    blob = bucket.get_blob(name)
    if blob:
        print(f"{name}: {blob.size} MiB")
```

### Filter by Size
```python
# Find large files
large_files = []
for name in bucket.names_blobs():
    blob = bucket.get_blob(name)
    if blob and blob.size > 100:  # > 100 MiB
        large_files.append(name)

print(f"Large files: {large_files}")
```

## API Reference

### Properties
| Property | Type | Description |
|----------|------|-------------|
| `name` | `str` | Blob name/path |
| `size` | `int` | Size in MiB (Mebibytes) |

## Size Conversion
```python
# Convert MiB to other units
size_mib = blob.size
size_bytes = blob.size * 1_048_576     # MiB to bytes
size_mb = blob.size * 1.048576         # MiB to MB (decimal)
size_gb = blob.size / 976.5625         # MiB to GB (decimal)
```

## Notes
- Size is returned in MiB (1 MiB = 1,048,576 bytes)
- Returns `None` if blob doesn't exist
- Minimal wrapper focused on basic properties