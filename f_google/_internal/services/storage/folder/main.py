from google.cloud.storage.bucket import Bucket as GBucket
from typing import List, Optional, Generator
from pathlib import Path
import os
from ..blob import Blob


class Folder:
    """
    ============================================================================
    PC-like folder abstraction for Google Cloud Storage (prefix-based).
    ============================================================================
    """

    def __init__(self, bucket: GBucket, path: str = '') -> None:
        """
        ========================================================================
        Initialize Folder with bucket and path.
        Args:
            bucket: Google Cloud Storage bucket
            path: Folder path (prefix) - should end with '/' for subfolders
        ========================================================================
        """
        self._bucket = bucket
        self._path = self._normalize_path(path)

    @property
    def name(self) -> str:
        """
        ========================================================================
        Get folder name (last part of path).
        ========================================================================
        """
        if not self._path:
            return ""
        return self._path.rstrip('/').split('/')[-1]

    @property
    def path(self) -> str:
        """
        ========================================================================
        Get full folder path.
        ========================================================================
        """
        return self._path

    @property
    def bucket_name(self) -> str:
        """
        ========================================================================
        Get bucket name this folder belongs to.
        ========================================================================
        """
        return self._bucket.name

    @property
    def parent(self) -> Optional['Folder']:
        """
        ========================================================================
        Get parent folder.
        ========================================================================
        """
        if not self._path or self._path == '/':
            return None
        
        parent_path = '/'.join(self._path.rstrip('/').split('/')[:-1])
        if parent_path:
            parent_path += '/'
        return Folder(self._bucket, parent_path)

    def exists(self) -> bool:
        """
        ========================================================================
        Check if folder exists (has any blobs with this prefix).
        ========================================================================
        """
        blobs = list(self._bucket.list_blobs(prefix=self._path, max_results=1))
        return len(blobs) > 0

    def list_files(self, recursive: bool = False) -> List[str]:
        """
        ========================================================================
        List files in this folder.
        Args:
            recursive: If True, include files in subfolders
        ========================================================================
        """
        if recursive:
            blobs = self._bucket.list_blobs(prefix=self._path)
            return [blob.name for blob in blobs if not blob.name.endswith('/')]
        else:
            blobs = self._bucket.list_blobs(prefix=self._path, delimiter='/')
            files = []
            for blob in blobs:
                if not blob.name.endswith('/'):
                    relative_name = blob.name[len(self._path):]
                    if '/' not in relative_name:
                        files.append(blob.name)
            return files

    def list_folders(self) -> List[str]:
        """
        ========================================================================
        List immediate subfolders in this folder.
        ========================================================================
        """
        iterator = self._bucket.list_blobs(prefix=self._path, delimiter='/')
        prefixes = set()
        for page in iterator.pages:
            if page.prefixes:
                for prefix in page.prefixes:
                    # Remove the current path and trailing slash to get folder name
                    folder_name = prefix[len(self._path):].rstrip('/')
                    if folder_name:
                        prefixes.add(prefix)
        return list(prefixes)

    def create_subfolder(self, subfolder_name: str) -> 'Folder':
        """
        ========================================================================
        Create a subfolder (conceptually - GCS doesn't have real folders).
        ========================================================================
        """
        subfolder_path = f"{self._path}{subfolder_name}/"
        return Folder(self._bucket, subfolder_path)

    def get_subfolder(self, subfolder_name: str) -> 'Folder':
        """
        ========================================================================
        Get a subfolder by name.
        ========================================================================
        """
        subfolder_path = f"{self._path}{subfolder_name}/"
        return Folder(self._bucket, subfolder_path)

    def get_file(self, file_name: str) -> Blob:
        """
        ========================================================================
        Get a file (blob) in this folder.
        ========================================================================
        """
        file_path = f"{self._path}{file_name}"
        blob = self._bucket.blob(file_path)
        return Blob(blob)

    def upload_file(self, local_file_path: str, remote_file_name: Optional[str] = None) -> Blob:
        """
        ========================================================================
        Upload a file to this folder.
        ========================================================================
        """
        if remote_file_name is None:
            remote_file_name = Path(local_file_path).name
        
        file_blob = self.get_file(remote_file_name)
        file_blob.upload_from_file(local_file_path)
        return file_blob

    def upload_string(self, content: str, file_name: str, content_type: str = 'text/plain') -> Blob:
        """
        ========================================================================
        Upload string content as a file to this folder.
        ========================================================================
        """
        file_blob = self.get_file(file_name)
        file_blob.upload_from_string(content, content_type=content_type)
        return file_blob

    def download_file(self, file_name: str, local_path: str) -> None:
        """
        ========================================================================
        Download a file from this folder to local path.
        ========================================================================
        """
        file_blob = self.get_file(file_name)
        file_blob.download_to_file(local_path)

    def delete_file(self, file_name: str) -> None:
        """
        ========================================================================
        Delete a file from this folder.
        ========================================================================
        """
        file_blob = self.get_file(file_name)
        file_blob.delete()

    def delete_folder(self, recursive: bool = False) -> None:
        """
        ========================================================================
        Delete this folder and optionally all its contents.
        ========================================================================
        """
        if recursive:
            # Delete all blobs with this prefix
            blobs = self._bucket.list_blobs(prefix=self._path)
            for blob in blobs:
                blob.delete()
        else:
            # Delete only files in this folder (not subfolders)
            files = self.list_files(recursive=False)
            for file_path in files:
                blob = self._bucket.blob(file_path)
                blob.delete()

    def copy_to(self, destination_folder: 'Folder', recursive: bool = False) -> None:
        """
        ========================================================================
        Copy this folder to another folder.
        ========================================================================
        """
        files = self.list_files(recursive=recursive)
        for file_path in files:
            # Get relative path from current folder
            relative_path = file_path[len(self._path):]
            
            # Create destination blob
            dest_blob_path = f"{destination_folder.path}{relative_path}"
            dest_blob = destination_folder._bucket.blob(dest_blob_path)
            
            # Copy content
            source_blob = self._bucket.blob(file_path)
            source_content = source_blob.download_as_bytes()
            dest_blob.upload_from_string(source_content)

    def move_to(self, destination_folder: 'Folder', recursive: bool = False) -> None:
        """
        ========================================================================
        Move this folder to another location.
        ========================================================================
        """
        self.copy_to(destination_folder, recursive=recursive)
        self.delete_folder(recursive=recursive)

    def sync_from_local(self, local_folder_path: str, recursive: bool = True) -> None:
        """
        ========================================================================
        Sync local folder to this remote folder.
        ========================================================================
        """
        local_path = Path(local_folder_path)
        if not local_path.exists():
            raise FileNotFoundError(f"Local folder not found: {local_folder_path}")
        
        if recursive:
            # Walk through all files and subdirectories
            for root, dirs, files in os.walk(local_folder_path):
                for file in files:
                    local_file_path = os.path.join(root, file)
                    # Get relative path from the base folder
                    relative_path = os.path.relpath(local_file_path, local_folder_path)
                    # Convert to forward slashes for GCS
                    relative_path = relative_path.replace('\\', '/')
                    
                    # Upload to remote folder
                    remote_blob_path = f"{self._path}{relative_path}"
                    blob = self._bucket.blob(remote_blob_path)
                    blob.upload_from_filename(local_file_path)
        else:
            # Only files in the immediate directory
            for file_path in local_path.glob('*'):
                if file_path.is_file():
                    self.upload_file(str(file_path))

    def sync_to_local(self, local_folder_path: str, recursive: bool = True) -> None:
        """
        ========================================================================
        Sync this remote folder to local folder.
        ========================================================================
        """
        local_path = Path(local_folder_path)
        local_path.mkdir(parents=True, exist_ok=True)
        
        files = self.list_files(recursive=recursive)
        for file_path in files:
            # Get relative path from current folder
            relative_path = file_path[len(self._path):]
            
            # Create local file path
            local_file_path = local_path / relative_path
            local_file_path.parent.mkdir(parents=True, exist_ok=True)
            
            # Download file
            blob = self._bucket.blob(file_path)
            blob.download_to_filename(str(local_file_path))

    def walk(self) -> Generator[tuple[str, List[str], List[str]], None, None]:
        """
        ========================================================================
        Walk through folder structure like os.walk().
        Yields: (folder_path, subfolders, files)
        ========================================================================
        """
        def _walk_recursive(current_path: str):
            folder = Folder(self._bucket, current_path)
            subfolders = folder.list_folders()
            files = folder.list_files(recursive=False)
            
            # Extract just the names from full paths
            subfolder_names = [f.rstrip('/').split('/')[-1] for f in subfolders]
            file_names = [f.split('/')[-1] for f in files]
            
            yield (current_path, subfolder_names, file_names)
            
            # Recursively walk subfolders
            for subfolder_path in subfolders:
                yield from _walk_recursive(subfolder_path)
        
        yield from _walk_recursive(self._path)

    def get_size(self, recursive: bool = True) -> int:
        """
        ========================================================================
        Get total size of all files in this folder.
        ========================================================================
        """
        total_size = 0
        files = self.list_files(recursive=recursive)
        for file_path in files:
            blob = self._bucket.blob(file_path)
            blob.reload()
            total_size += blob.size or 0
        return total_size

    def get_file_count(self, recursive: bool = True) -> int:
        """
        ========================================================================
        Get total number of files in this folder.
        ========================================================================
        """
        return len(self.list_files(recursive=recursive))

    def _normalize_path(self, path: str) -> str:
        """
        ========================================================================
        Normalize folder path to ensure consistent format.
        ========================================================================
        """
        if not path:
            return ''
        
        # Remove leading slash, ensure trailing slash for non-empty paths
        path = path.lstrip('/')
        if path and not path.endswith('/'):
            path += '/'
        
        return path

    def __str__(self) -> str:
        """
        ========================================================================
        String representation of the folder.
        ========================================================================
        """
        return f"Folder(path='{self._path}', bucket='{self.bucket_name}')"

    def __repr__(self) -> str:
        """
        ========================================================================
        Detailed representation of the folder.
        ========================================================================
        """
        return f"Folder(path='{self._path}', bucket='{self.bucket_name}', files={self.get_file_count()})"

    def __contains__(self, item: str) -> bool:
        """
        ========================================================================
        Check if file or folder exists in this folder.
        ========================================================================
        """
        # Check if it's a file
        files = self.list_files(recursive=False)
        for file_path in files:
            if file_path.split('/')[-1] == item:
                return True
        
        # Check if it's a subfolder
        folders = self.list_folders()
        for folder_path in folders:
            if folder_path.rstrip('/').split('/')[-1] == item:
                return True
        
        return False

    def __len__(self) -> int:
        """
        ========================================================================
        Get total number of files and folders in this folder.
        ========================================================================
        """
        return len(self.list_files(recursive=False)) + len(self.list_folders())