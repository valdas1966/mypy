from google.cloud.storage.blob import Blob as GBlob
from google.cloud.storage.bucket import Bucket as GBucket
from typing import Optional, Dict, Any, IO
import requests
from pathlib import Path
import io


class Blob:
    """
    ============================================================================
    Enhanced Google Cloud Storage blob wrapper with advanced operations.
    ============================================================================
    """

    def __init__(self, g_blob: GBlob) -> None:
        """
        ========================================================================
        Initialize Blob wrapper with Google Cloud Storage blob instance.
        ========================================================================
        """
        self._blob = g_blob
        self._metadata_cache: Optional[Dict[str, Any]] = None

    @property
    def name(self) -> str:
        """
        ========================================================================
        Get blob name.
        ========================================================================
        """
        return self._blob.name

    @property
    def bucket_name(self) -> str:
        """
        ========================================================================
        Get bucket name this blob belongs to.
        ========================================================================
        """
        return self._blob.bucket.name

    @property
    def size(self) -> int:
        """
        ========================================================================
        Get blob size in bytes (cached for performance).
        ========================================================================
        """
        if self._metadata_cache is None:
            self._load_metadata()
        return self._blob.size

    @property
    def content_type(self) -> str:
        """
        ========================================================================
        Get blob content type.
        ========================================================================
        """
        if self._metadata_cache is None:
            self._load_metadata()
        return self._blob.content_type or 'application/octet-stream'

    @property
    def etag(self) -> str:
        """
        ========================================================================
        Get blob ETag for versioning.
        ========================================================================
        """
        if self._metadata_cache is None:
            self._load_metadata()
        return self._blob.etag

    @property
    def public_url(self) -> str:
        """
        ========================================================================
        Get public URL for the blob.
        ========================================================================
        """
        return self._blob.public_url

    def exists(self) -> bool:
        """
        ========================================================================
        Check if blob exists in the bucket.
        ========================================================================
        """
        return self._blob.exists()

    def delete(self) -> None:
        """
        ========================================================================
        Delete the blob from storage.
        ========================================================================
        """
        self._blob.delete()
        self._metadata_cache = None

    def download_to_file(self, file_path: str) -> None:
        """
        ========================================================================
        Download blob content to a local file.
        ========================================================================
        """
        with open(file_path, 'wb') as file_obj:
            self._blob.download_to_file(file_obj)

    def download_as_bytes(self) -> bytes:
        """
        ========================================================================
        Download blob content as bytes.
        ========================================================================
        """
        return self._blob.download_as_bytes()

    def download_as_text(self, encoding: str = 'utf-8') -> str:
        """
        ========================================================================
        Download blob content as text.
        ========================================================================
        """
        return self._blob.download_as_text(encoding=encoding)

    def upload_from_file(self, file_path: str, content_type: Optional[str] = None) -> None:
        """
        ========================================================================
        Upload content from a local file.
        ========================================================================
        """
        if content_type:
            self._blob.content_type = content_type
        with open(file_path, 'rb') as file_obj:
            self._blob.upload_from_file(file_obj)
        self._metadata_cache = None

    def upload_from_string(self, data: str, content_type: Optional[str] = None) -> None:
        """
        ========================================================================
        Upload content from a string.
        ========================================================================
        """
        if content_type:
            self._blob.content_type = content_type
        self._blob.upload_from_string(data)
        self._metadata_cache = None

    def upload_from_bytes(self, data: bytes, content_type: Optional[str] = None) -> None:
        """
        ========================================================================
        Upload content from bytes.
        ========================================================================
        """
        if content_type:
            self._blob.content_type = content_type
        self._blob.upload_from_string(data)
        self._metadata_cache = None

    def upload_from_url(self, url: str, content_type: Optional[str] = None) -> None:
        """
        ========================================================================
        Upload content from a URL.
        ========================================================================
        """
        response = requests.get(url)
        response.raise_for_status()
        
        if content_type:
            self._blob.content_type = content_type
        self._blob.upload_from_string(response.content)
        self._metadata_cache = None

    def copy_to(self, destination_blob_name: str, destination_bucket: Optional[GBucket] = None) -> 'Blob':
        """
        ========================================================================
        Copy blob to another location.
        ========================================================================
        """
        if destination_bucket is None:
            destination_bucket = self._blob.bucket
        
        destination_blob = destination_bucket.blob(destination_blob_name)
        destination_blob.upload_from_string(self.download_as_bytes())
        return Blob(destination_blob)

    def move_to(self, destination_blob_name: str, destination_bucket: Optional[GBucket] = None) -> 'Blob':
        """
        ========================================================================
        Move blob to another location.
        ========================================================================
        """
        new_blob = self.copy_to(destination_blob_name, destination_bucket)
        self.delete()
        return new_blob

    def get_metadata(self) -> Dict[str, Any]:
        """
        ========================================================================
        Get blob metadata.
        ========================================================================
        """
        if self._metadata_cache is None:
            self._load_metadata()
        return {
            'name': self.name,
            'bucket': self.bucket_name,
            'size': self.size,
            'content_type': self.content_type,
            'etag': self.etag,
            'created': self._blob.time_created,
            'updated': self._blob.updated,
            'public_url': self.public_url
        }

    def set_metadata(self, metadata: Dict[str, str]) -> None:
        """
        ========================================================================
        Set custom metadata for the blob.
        ========================================================================
        """
        self._blob.metadata = metadata
        self._blob.patch()
        self._metadata_cache = None

    def make_public(self) -> None:
        """
        ========================================================================
        Make blob publicly accessible.
        ========================================================================
        """
        self._blob.make_public()

    def make_private(self) -> None:
        """
        ========================================================================
        Make blob private.
        ========================================================================
        """
        self._blob.make_private()

    def generate_signed_url(self, expiration_minutes: int = 60) -> str:
        """
        ========================================================================
        Generate a signed URL for temporary access.
        ========================================================================
        """
        from datetime import datetime, timedelta
        expiration = datetime.utcnow() + timedelta(minutes=expiration_minutes)
        return self._blob.generate_signed_url(expiration)

    def stream_download(self) -> IO[bytes]:
        """
        ========================================================================
        Get a stream for downloading large files.
        ========================================================================
        """
        stream = io.BytesIO()
        self._blob.download_to_file(stream)
        stream.seek(0)
        return stream

    def _load_metadata(self) -> None:
        """
        ========================================================================
        Load blob metadata from storage.
        ========================================================================
        """
        self._blob.reload()
        self._metadata_cache = True

    def __str__(self) -> str:
        """
        ========================================================================
        String representation of the blob.
        ========================================================================
        """
        return f"Blob(name='{self.name}', bucket='{self.bucket_name}')"

    def __repr__(self) -> str:
        """
        ========================================================================
        Detailed representation of the blob.
        ========================================================================
        """
        return f"Blob(name='{self.name}', bucket='{self.bucket_name}', size={self.size})"