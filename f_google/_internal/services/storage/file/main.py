from google.cloud.storage.blob import Blob as GBlob
from google.cloud.storage.bucket import Bucket as GBucket
from typing import Optional, Dict, Any, IO
from pathlib import Path
import os
from ..blob import Blob


class File:
    """
    ============================================================================
    PC-like file abstraction for Google Cloud Storage blobs.
    ============================================================================
    """

    def __init__(self, bucket: GBucket, file_path: str) -> None:
        """
        ========================================================================
        Initialize File with bucket and file path.
        Args:
            bucket: Google Cloud Storage bucket
            file_path: Full path to the file (blob name)
        ========================================================================
        """
        self._bucket = bucket
        self._path = file_path
        self._blob = Blob(bucket.blob(file_path))

    @property
    def name(self) -> str:
        """
        ========================================================================
        Get file name (last part of path).
        ========================================================================
        """
        return Path(self._path).name

    @property
    def stem(self) -> str:
        """
        ========================================================================
        Get file name without extension.
        ========================================================================
        """
        return Path(self._path).stem

    @property
    def suffix(self) -> str:
        """
        ========================================================================
        Get file extension.
        ========================================================================
        """
        return Path(self._path).suffix

    @property
    def path(self) -> str:
        """
        ========================================================================
        Get full file path.
        ========================================================================
        """
        return self._path

    @property
    def parent_path(self) -> str:
        """
        ========================================================================
        Get parent directory path.
        ========================================================================
        """
        return '/'.join(self._path.split('/')[:-1])

    @property
    def bucket_name(self) -> str:
        """
        ========================================================================
        Get bucket name this file belongs to.
        ========================================================================
        """
        return self._bucket.name

    @property
    def size(self) -> int:
        """
        ========================================================================
        Get file size in bytes.
        ========================================================================
        """
        return self._blob.size

    @property
    def content_type(self) -> str:
        """
        ========================================================================
        Get file content type.
        ========================================================================
        """
        return self._blob.content_type

    @property
    def public_url(self) -> str:
        """
        ========================================================================
        Get public URL for the file.
        ========================================================================
        """
        return self._blob.public_url

    def exists(self) -> bool:
        """
        ========================================================================
        Check if file exists.
        ========================================================================
        """
        return self._blob.exists()

    def delete(self) -> None:
        """
        ========================================================================
        Delete the file.
        ========================================================================
        """
        self._blob.delete()

    def read_text(self, encoding: str = 'utf-8') -> str:
        """
        ========================================================================
        Read file content as text.
        ========================================================================
        """
        return self._blob.download_as_text(encoding=encoding)

    def read_bytes(self) -> bytes:
        """
        ========================================================================
        Read file content as bytes.
        ========================================================================
        """
        return self._blob.download_as_bytes()

    def write_text(self, content: str, encoding: str = 'utf-8', content_type: Optional[str] = None) -> None:
        """
        ========================================================================
        Write text content to file.
        ========================================================================
        """
        if content_type is None:
            content_type = self._guess_content_type()
        self._blob.upload_from_string(content, content_type=content_type)

    def write_bytes(self, content: bytes, content_type: Optional[str] = None) -> None:
        """
        ========================================================================
        Write bytes content to file.
        ========================================================================
        """
        if content_type is None:
            content_type = self._guess_content_type()
        self._blob.upload_from_bytes(content, content_type=content_type)

    def copy_from_local(self, local_file_path: str, content_type: Optional[str] = None) -> None:
        """
        ========================================================================
        Copy content from local file.
        ========================================================================
        """
        if content_type is None:
            content_type = self._guess_content_type()
        self._blob.upload_from_file(local_file_path, content_type=content_type)

    def copy_to_local(self, local_file_path: str) -> None:
        """
        ========================================================================
        Copy file content to local file.
        ========================================================================
        """
        # Create parent directories if they don't exist
        local_path = Path(local_file_path)
        local_path.parent.mkdir(parents=True, exist_ok=True)
        
        self._blob.download_to_file(str(local_path))

    def copy_from_url(self, url: str, content_type: Optional[str] = None) -> None:
        """
        ========================================================================
        Copy content from URL.
        ========================================================================
        """
        if content_type is None:
            content_type = self._guess_content_type()
        self._blob.upload_from_url(url, content_type=content_type)

    def copy_to(self, destination_path: str, destination_bucket: Optional[GBucket] = None) -> 'File':
        """
        ========================================================================
        Copy file to another location.
        ========================================================================
        """
        if destination_bucket is None:
            destination_bucket = self._bucket
        
        destination_file = File(destination_bucket, destination_path)
        content = self.read_bytes()
        destination_file.write_bytes(content, content_type=self.content_type)
        return destination_file

    def move_to(self, destination_path: str, destination_bucket: Optional[GBucket] = None) -> 'File':
        """
        ========================================================================
        Move file to another location.
        ========================================================================
        """
        new_file = self.copy_to(destination_path, destination_bucket)
        self.delete()
        return new_file

    def rename(self, new_name: str) -> 'File':
        """
        ========================================================================
        Rename file (move to new name in same directory).
        ========================================================================
        """
        new_path = f"{self.parent_path}/{new_name}" if self.parent_path else new_name
        return self.move_to(new_path)

    def backup(self, backup_suffix: str = '.bak') -> 'File':
        """
        ========================================================================
        Create backup copy of file.
        ========================================================================
        """
        backup_path = f"{self._path}{backup_suffix}"
        return self.copy_to(backup_path)

    def get_metadata(self) -> Dict[str, Any]:
        """
        ========================================================================
        Get file metadata.
        ========================================================================
        """
        return self._blob.get_metadata()

    def set_metadata(self, metadata: Dict[str, str]) -> None:
        """
        ========================================================================
        Set custom metadata for the file.
        ========================================================================
        """
        self._blob.set_metadata(metadata)

    def make_public(self) -> None:
        """
        ========================================================================
        Make file publicly accessible.
        ========================================================================
        """
        self._blob.make_public()

    def make_private(self) -> None:
        """
        ========================================================================
        Make file private.
        ========================================================================
        """
        self._blob.make_private()

    def generate_signed_url(self, expiration_minutes: int = 60) -> str:
        """
        ========================================================================
        Generate a signed URL for temporary access.
        ========================================================================
        """
        return self._blob.generate_signed_url(expiration_minutes)

    def get_download_stream(self) -> IO[bytes]:
        """
        ========================================================================
        Get a stream for downloading large files.
        ========================================================================
        """
        return self._blob.stream_download()

    def append_text(self, content: str, encoding: str = 'utf-8') -> None:
        """
        ========================================================================
        Append text content to file.
        Note: This downloads, appends, and re-uploads the entire file.
        ========================================================================
        """
        try:
            existing_content = self.read_text(encoding=encoding)
            new_content = existing_content + content
        except:
            # File doesn't exist, create with new content
            new_content = content
        
        self.write_text(new_content, encoding=encoding)

    def append_bytes(self, content: bytes) -> None:
        """
        ========================================================================
        Append bytes content to file.
        Note: This downloads, appends, and re-uploads the entire file.
        ========================================================================
        """
        try:
            existing_content = self.read_bytes()
            new_content = existing_content + content
        except:
            # File doesn't exist, create with new content
            new_content = content
        
        self.write_bytes(new_content)

    def is_text_file(self) -> bool:
        """
        ========================================================================
        Check if file is likely a text file based on content type and extension.
        ========================================================================
        """
        text_extensions = {'.txt', '.md', '.py', '.js', '.html', '.css', '.json', '.xml', '.csv', '.log'}
        text_content_types = {'text/', 'application/json', 'application/xml'}
        
        # Check by extension
        if self.suffix.lower() in text_extensions:
            return True
        
        # Check by content type
        content_type = self.content_type.lower()
        return any(content_type.startswith(prefix) for prefix in text_content_types)

    def is_image_file(self) -> bool:
        """
        ========================================================================
        Check if file is an image based on content type and extension.
        ========================================================================
        """
        image_extensions = {'.jpg', '.jpeg', '.png', '.gif', '.bmp', '.webp', '.svg'}
        
        # Check by extension
        if self.suffix.lower() in image_extensions:
            return True
        
        # Check by content type
        return self.content_type.lower().startswith('image/')

    def get_file_type(self) -> str:
        """
        ========================================================================
        Get file type category.
        ========================================================================
        """
        if self.is_text_file():
            return 'text'
        elif self.is_image_file():
            return 'image'
        elif self.content_type.startswith('video/'):
            return 'video'
        elif self.content_type.startswith('audio/'):
            return 'audio'
        elif self.content_type.startswith('application/'):
            return 'application'
        else:
            return 'binary'

    def _guess_content_type(self) -> str:
        """
        ========================================================================
        Guess content type based on file extension.
        ========================================================================
        """
        import mimetypes
        content_type, _ = mimetypes.guess_type(self._path)
        return content_type or 'application/octet-stream'

    def __str__(self) -> str:
        """
        ========================================================================
        String representation of the file.
        ========================================================================
        """
        return f"File(path='{self._path}', bucket='{self.bucket_name}')"

    def __repr__(self) -> str:
        """
        ========================================================================
        Detailed representation of the file.
        ========================================================================
        """
        return f"File(path='{self._path}', bucket='{self.bucket_name}', size={self.size})"

    def __eq__(self, other) -> bool:
        """
        ========================================================================
        Check if two files are equal (same path and bucket).
        ========================================================================
        """
        if not isinstance(other, File):
            return False
        return self._path == other._path and self.bucket_name == other.bucket_name

    def __hash__(self) -> int:
        """
        ========================================================================
        Hash function for file objects.
        ========================================================================
        """
        return hash((self._path, self.bucket_name))