# Google Cloud Storage Module

## Overview
This module provides a comprehensive wrapper for Google Cloud Storage operations, featuring bucket management, blob operations, and seamless integration with the existing authentication system. It supports file uploads from local PC and URLs, downloads, and full bucket lifecycle management.

## Architecture

### Folder Structure
```
f_google/_internal/services/storage/
├── __init__.py          # Main exports
├── main.py              # Storage class
├── bucket/              # Bucket component
│   ├── __init__.py      # Bucket exports
│   ├── main.py          # Bucket class
│   ├── _factory.py      # Bucket factory methods
│   └── _tester.py       # Bucket-specific tests
├── blob/                # Blob wrapper component
│   ├── __init__.py      # Blob exports
│   ├── main.py          # Blob class
│   ├── _factory.py      # Blob factory methods
│   └── _tester.py       # Blob-specific tests
├── folder/              # Folder abstraction component
│   ├── __init__.py      # Folder exports
│   ├── main.py          # Folder class
│   ├── _factory.py      # Folder factory methods
│   └── _tester.py       # Folder-specific tests
├── file/                # File abstraction component
│   ├── __init__.py      # File exports
│   ├── main.py          # File class
│   ├── _factory.py      # File factory methods
│   └── _tester.py       # File-specific tests
├── _factory.py          # Storage factory methods
├── _tester.py           # Storage-level tests
└── claude.md            # This documentation
```

### Core Components

#### `main.py` - Storage Class
- **Purpose**: Main storage client with bucket management capabilities
- **Key Features**:
  - List, create, and delete buckets
  - Dictionary-style bucket access via `__getitem__`
  - Integrated with authentication system
  - Returns wrapped `Bucket` instances

#### `bucket/main.py` - Bucket Class
- **Purpose**: Wrapper for individual bucket operations
- **Key Features**:
  - List, upload, download, and delete blobs
  - Upload from local files or URLs
  - Blob existence checking and metadata
  - Pythonic interfaces (`__len__`, `__contains__`)

#### `_factory.py` - Storage Factory Class
- **Purpose**: Convenience factory methods for storage instances
- **Methods**:
  - `rami()`: Storage with RAMI service account
  - `valdas()`: Storage with VALDAS service account
  - `from_account()`: Storage with specified service account

#### `bucket/_factory.py` - Bucket Factory Class
- **Purpose**: Convenience factory methods for bucket instances
- **Methods**:
  - `rami(bucket_name)`: Bucket with RAMI service account
  - `valdas(bucket_name)`: Bucket with VALDAS service account
  - `from_name(bucket_name, account)`: Bucket with specified account

#### `blob/main.py` - Blob Wrapper Class
- **Purpose**: Enhanced blob operations with advanced features
- **Key Features**:
  - Metadata caching and operations
  - Multiple upload/download methods
  - Copy, move, and URL operations
  - Streaming support and signed URLs

#### `folder/main.py` - Folder Abstraction Class
- **Purpose**: PC-like folder operations for GCS prefixes
- **Key Features**:
  - Directory-style navigation and listing
  - Sync operations with local folders
  - Recursive operations and folder walking
  - Parent/child folder relationships

#### `file/main.py` - File Abstraction Class
- **Purpose**: PC-like file operations for individual blobs
- **Key Features**:
  - Text and binary read/write operations
  - File type detection and metadata
  - Copy, move, rename, and backup operations
  - Local file integration and streaming

#### `_tester.py` - Storage Testing Functions
- **Purpose**: Storage-level testing suite
- **Tests**: Connection, bucket access, factory patterns, integration

#### `bucket/_tester.py` - Bucket Testing Functions
- **Purpose**: Bucket-specific testing suite
- **Tests**: Blob operations, file upload/download, bucket properties

#### `blob/_tester.py` - Blob Testing Functions
- **Purpose**: Blob-specific testing suite
- **Tests**: Enhanced blob operations, metadata, copy/move, URL operations

#### `folder/_tester.py` - Folder Testing Functions
- **Purpose**: Folder-specific testing suite
- **Tests**: Directory operations, sync operations, folder walking

#### `file/_tester.py` - File Testing Functions
- **Purpose**: File-specific testing suite
- **Tests**: File operations, text/binary handling, local integration

## Usage Examples

### Basic Storage Operations

```python
from f_google.services.storage import Storage

# Create storage instance with factory
storage = Storage.Factory.rami()

# List all buckets
buckets = storage.list_buckets()
print(f"Available buckets: {buckets}")

# Access bucket using dictionary syntax
bucket = storage['my-bucket-name']

# Or use explicit method
bucket = storage.get_bucket('my-bucket-name')
```

### Bucket Management

```python
# Create a new bucket
new_bucket = storage.create_bucket('my-new-bucket', location='US')

# Delete a bucket (empty bucket only)
storage.delete_bucket('my-old-bucket')

# Force delete bucket with all contents
storage.delete_bucket('my-old-bucket', force=True)
```

### Blob Operations

```python
# Get bucket
bucket = storage['my-bucket']

# List all blobs
blobs = bucket.list_blobs()
print(f"Found {len(blobs)} blobs")

# List blobs with prefix
filtered_blobs = bucket.list_blobs(prefix='uploads/')

# Upload file from local PC
bucket.upload_file('/path/to/local/file.txt', 'destination/file.txt')

# Upload file from URL
bucket.upload_from_url('https://example.com/file.pdf', 'downloaded/file.pdf')

# Download g_blob to local PC
bucket.download_blob('remote/file.txt', '/path/to/local/file.txt')

# Delete a g_blob
bucket.delete_blob('unwanted/file.txt')
```

### Advanced Blob Operations

```python
# Check if g_blob exists
if 'important.txt' in bucket:
    print("File exists!")

# Get g_blob size
size = bucket.get_blob_size('large-file.zip')
print(f"File size: {size} bytes")

# Get public URL
url = bucket.get_blob_url('public-file.jpg')
print(f"Public URL: {url}")

# Get bucket info
print(f"Bucket has {len(bucket)} blobs")
```

### Factory Pattern Usage

```python
from f_google.services.storage import Storage

# Quick access to different service accounts
rami_storage = Storage.Factory.rami()
valdas_storage = Storage.Factory.valdas()

# Generic factory method
from f_google.auth import ServiceAccount

storage = Storage.Factory.from_account(ServiceAccount.RAMI)
```

### Bucket Factory Usage

```python
from f_google.services.storage.bucket import Bucket

# Direct bucket access with factory
bucket = Bucket.Factory.rami('my-bucket-name')

# Or using different accounts
bucket = Bucket.Factory.valdas('my-bucket-name')
bucket = Bucket.Factory.from_name('my-bucket-name', ServiceAccount.RAMI)
```

### File System Abstraction Usage

```python
from f_google.services.storage import Storage

# Get storage and bucket
storage = Storage.Factory.rami()
bucket = storage['my-bucket']

# Work with folders like PC directories
folder = bucket.folder('documents/reports/')
folder.upload_file('/local/report.pdf', 'monthly-report.pdf')
files = folder.list_files()
subfolders = folder.list_folders()

# Work with files like PC files
file = bucket.file('documents/report.pdf')
content = file.read_text()
file.copy_to('backup/report.pdf')
file.make_public()

# Work with enhanced blobs
blob = bucket.blob('data/file.json')
metadata = blob.get_metadata()
blob.copy_to('archive/file.json')
```

### Advanced File Operations

```python
# File operations
file = bucket.file('documents/notes.txt')
file.write_text("Hello, World!")
file.append_text("\nMore content")
content = file.read_text()

# Copy operations
file.copy_to('backup/notes.txt')
file.move_to('archive/notes.txt')
file.rename('new-notes.txt')
backup = file.backup('.bak')

# Local integration
file.copy_from_local('/local/file.txt')
file.copy_to_local('/local/downloaded.txt')
```

### Folder Sync Operations

```python
# Folder operations
folder = bucket.folder('projects/')

# Sync with local directories
folder.sync_from_local('/local/projects/', recursive=True)
folder.sync_to_local('/backup/projects/', recursive=True)

# Navigate folder structure
subfolder = folder.create_subfolder('new-project')
parent = folder.parent
root = bucket.root

# Walk through folder structure
for folder_path, subfolders, files in bucket.walk():
    print(f"Folder: {folder_path}")
    print(f"  Subfolders: {subfolders}")
    print(f"  Files: {files}")
```

### Direct Component Access

```python
# Direct component factories
from f_google.services.storage.bucket.blob import Blob
from f_google.services.storage import Folder
from f_google.services.storage import File

# Direct g_blob access
blob = Blob.Factory.rami('bucket-name', 'g_blob-name')
blob.upload_from_url('https://example.com/file.pdf')

# Direct folder access
folder = Folder.Factory.rami('bucket-name', 'folder-path/')
folder.upload_string("content", "file.txt")

# Direct file access
file = File.Factory.rami('bucket-name', 'file-path.txt')
file.write_text("Hello, World!")
```

## API Reference

### Storage Class Methods

| Method | Description | Parameters | Returns |
|--------|-------------|------------|---------|
| `list_buckets()` | List all accessible buckets | None | `list[str]` |
| `create_bucket(name, location)` | Create new bucket | `name: str`, `location: str = 'US'` | `Bucket` |
| `delete_bucket(name, force)` | Delete bucket | `name: str`, `force: bool = False` | `None` |
| `get_bucket(name)` | Get bucket by name | `name: str` | `Bucket` |
| `__getitem__(name)` | Dictionary-style access | `name: str` | `Bucket` |

### Bucket Class Methods

| Method | Description | Parameters | Returns |
|--------|-------------|------------|---------|
| `list_blobs(prefix)` | List blobs with optional prefix | `prefix: Optional[str] = None` | `list[str]` |
| `upload_file(local_path, blob_name)` | Upload from local file | `local_path: str`, `blob_name: Optional[str] = None` | `None` |
| `upload_from_url(url, blob_name)` | Upload from URL | `url: str`, `blob_name: str` | `None` |
| `download_blob(blob_name, local_path)` | Download to local file | `blob_name: str`, `local_path: str` | `None` |
| `delete_blob(blob_name)` | Delete blob | `blob_name: str` | `None` |
| `blob_exists(blob_name)` | Check if blob exists | `blob_name: str` | `bool` |
| `get_blob_size(blob_name)` | Get blob size | `blob_name: str` | `int` |
| `get_blob_url(blob_name)` | Get public URL | `blob_name: str` | `str` |
| `__len__()` | Get total blob count | None | `int` |
| `__contains__(blob_name)` | Check existence with 'in' | `blob_name: str` | `bool` |

### Storage Factory Class Methods

| Method | Description | Returns |
|--------|-------------|---------|
| `rami()` | Storage with RAMI account | `Storage` |
| `valdas()` | Storage with VALDAS account | `Storage` |
| `from_account(account)` | Storage with specified account | `Storage` |

### Bucket Factory Class Methods

| Method | Description | Parameters | Returns |
|--------|-------------|------------|---------|
| `rami(bucket_name)` | Bucket with RAMI account | `bucket_name: str` | `Bucket` |
| `valdas(bucket_name)` | Bucket with VALDAS account | `bucket_name: str` | `Bucket` |
| `from_name(bucket_name, account)` | Bucket with specified account | `bucket_name: str`, `account: ServiceAccount` | `Bucket` |
| `from_g_bucket(g_bucket)` | Bucket from Google bucket | `g_bucket: GBucket` | `Bucket` |

### Blob Factory Class Methods

| Method | Description | Parameters | Returns |
|--------|-------------|------------|---------|
| `rami(bucket_name, blob_name)` | Blob with RAMI account | `bucket_name: str`, `blob_name: str` | `Blob` |
| `valdas(bucket_name, blob_name)` | Blob with VALDAS account | `bucket_name: str`, `blob_name: str` | `Blob` |
| `from_path(bucket_name, blob_name, account)` | Blob with specified account | `bucket_name: str`, `blob_name: str`, `account: ServiceAccount` | `Blob` |
| `from_g_blob(g_blob)` | Blob from Google blob | `g_blob: GBlob` | `Blob` |

### Folder Factory Class Methods

| Method | Description | Parameters | Returns |
|--------|-------------|------------|---------|
| `rami(bucket_name, folder_path)` | Folder with RAMI account | `bucket_name: str`, `folder_path: str = ''` | `Folder` |
| `valdas(bucket_name, folder_path)` | Folder with VALDAS account | `bucket_name: str`, `folder_path: str = ''` | `Folder` |
| `from_path(bucket_name, folder_path, account)` | Folder with specified account | `bucket_name: str`, `folder_path: str`, `account: ServiceAccount` | `Folder` |
| `root_rami(bucket_name)` | Root folder with RAMI account | `bucket_name: str` | `Folder` |
| `root_valdas(bucket_name)` | Root folder with VALDAS account | `bucket_name: str` | `Folder` |

### File Factory Class Methods

| Method | Description | Parameters | Returns |
|--------|-------------|------------|---------|
| `rami(bucket_name, file_path)` | File with RAMI account | `bucket_name: str`, `file_path: str` | `File` |
| `valdas(bucket_name, file_path)` | File with VALDAS account | `bucket_name: str`, `file_path: str` | `File` |
| `from_path(bucket_name, file_path, account)` | File with specified account | `bucket_name: str`, `file_path: str`, `account: ServiceAccount` | `File` |
| `create_new_rami(bucket_name, file_path)` | New file with RAMI account | `bucket_name: str`, `file_path: str` | `File` |
| `create_new_valdas(bucket_name, file_path)` | New file with VALDAS account | `bucket_name: str`, `file_path: str` | `File` |

## Error Handling

### Common Exceptions

1. **Authentication Errors**: Invalid credentials or missing permissions
2. **Bucket Not Found**: Accessing non-existent bucket
3. **Blob Not Found**: Accessing non-existent blob
4. **Permission Denied**: Insufficient permissions for operation
5. **Network Errors**: Connection issues or timeouts

### Example Error Handling

```python
from google.cloud.exceptions import NotFound, Forbidden

try:
    bucket = storage['non-existent-bucket']
    bucket.upload_file('/local/file.txt', 'remote/file.txt')
except NotFound:
    print("Bucket not found")
except Forbidden:
    print("Permission denied")
except Exception as e:
    print(f"Unexpected error: {e}")
```

## Testing

### Running Tests

```python
# Run storage-level tests
from f_google.services.storage._tester import run_all_tests

run_all_tests()

# Run bucket-specific tests
from f_google.services.storage.bucket._tester import run_all_tests

run_all_tests()

# Run specific tests
from f_google.services.storage._tester import test_storage_connection

test_storage_connection()

from f_google.services.storage.bucket._tester import test_blob_operations

test_blob_operations()
```

### Test Coverage

#### Storage-Level Tests
- **Connection Testing**: Verify authentication and basic connectivity
- **Bucket Operations**: Test listing, creation, deletion, and access
- **Factory Patterns**: Test different service account access methods
- **Integration**: Test storage and bucket wrapper integration

#### Bucket-Level Tests
- **Blob Operations**: Test upload, download, deletion, and metadata
- **Factory Patterns**: Test bucket-specific factory methods
- **Properties**: Test bucket properties and methods
- **File System Integration**: Test integration with blob, folder, and file abstractions

#### Blob-Level Tests
- **Enhanced Operations**: Test metadata caching, streaming, and advanced operations
- **Copy/Move Operations**: Test blob copying and moving functionality
- **URL Operations**: Test signed URLs, public access, and URL uploads
- **Factory Patterns**: Test blob-specific factory methods

#### Folder-Level Tests
- **Directory Operations**: Test folder navigation, listing, and creation
- **Sync Operations**: Test local folder synchronization
- **Folder Walking**: Test recursive folder traversal
- **Parent/Child Navigation**: Test folder relationship operations

#### File-Level Tests
- **Text/Binary Operations**: Test file reading, writing, and appending
- **Local Integration**: Test local file copying and synchronization
- **File Operations**: Test copy, move, rename, and backup operations
- **Type Detection**: Test file type detection and metadata handling

## Dependencies

- `google-cloud-storage`: Google's official Cloud Storage client
- `requests`: For URL-based uploads
- `pathlib`: For file path operations
- `tempfile`: For testing file operations

## Security Considerations

1. **Service Account Permissions**: Ensure service accounts have appropriate Storage permissions
2. **Bucket Policies**: Configure bucket access policies according to security requirements
3. **Data Encryption**: Consider encryption for sensitive data
4. **Access Logging**: Enable Cloud Storage access logging for audit trails

## Performance Considerations

1. **Batch Operations**: Use batch operations for multiple blob operations
2. **Parallel Uploads**: Consider parallel uploads for large files
3. **Streaming**: Use streaming for large file downloads
4. **Caching**: Implement caching for frequently accessed metadata

## Integration Examples

### With Data Processing Pipeline

```python
# Process and upload results
storage = Storage.Factory.rami()
bucket = storage['processing-results']

# Upload processed data
bucket.upload_file('/tmp/processed_data.csv', 'results/daily_report.csv')

# Download for further processing
bucket.download_blob('raw_data.json', '/tmp/input.json')
```

### With Web Application

```python
# Handle file uploads in web app
def handle_file_upload(file_data, filename):
    storage = Storage.Factory.valdas()
    bucket = storage['user-uploads']
    
    # Upload user file
    bucket.upload_file(file_data, f'users/{user_id}/{filename}')
    
    # Get public URL
    return bucket.get_blob_url(f'users/{user_id}/{filename}')
```

## Extension Guidelines

### Adding New Storage Features

1. **Extend Bucket Class**: Add new methods to `_bucket.py`
2. **Update Tests**: Add corresponding tests in `_tester.py`
3. **Document Changes**: Update this documentation
4. **Version Compatibility**: Ensure backward compatibility

### Custom Storage Patterns

```python
# Example: Custom backup pattern
class BackupStorage(Storage):
    def backup_directory(self, local_dir: str, bucket_name: str):
        bucket = self[bucket_name]
        # Implementation for directory backup
        pass
```

## Troubleshooting

### Common Issues

1. **Import Errors**: Ensure all dependencies are installed
2. **Authentication Failed**: Check service account credentials
3. **Bucket Access Denied**: Verify bucket permissions
4. **Network Timeouts**: Check network connectivity
5. **Quota Exceeded**: Monitor storage quotas and billing

### Debug Mode

```python
# Enable debug logging
import logging
logging.basicConfig(level=logging.DEBUG)

# Test connection with verbose output
test_storage_connection()
```

## Best Practices

1. **Use Factory Pattern**: Prefer factory methods over direct instantiation
2. **Handle Exceptions**: Always wrap operations in try-catch blocks
3. **Clean Up Resources**: Delete temporary files and test buckets
4. **Monitor Costs**: Track storage usage and data transfer costs
5. **Security First**: Follow principle of least privilege for service accounts

This comprehensive storage module provides a robust foundation for Google Cloud Storage operations while maintaining consistency with the existing codebase architecture.