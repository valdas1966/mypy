from google.cloud.storage.bucket import Bucket as GBucket
from f_google.strategies.retry import Retry
from f_google.storage.blob import Blob
from f_os import old_u_file, u_folder


class Bucket:
    """
    ============================================================================
     Google-Storage Bucket.
    ============================================================================
    """

    def __init__(self,
                 bucket: GBucket,
                 verbose: bool = True) -> None:
        """
        ========================================================================
         Init private Attributes.
        ========================================================================
        """
        self._bucket: GBucket = bucket
        self._verbose = verbose

    def folders(self, folder: str = None) -> list[str]:
        """
        ========================================================================
         1. Return a list of top-level english within a specified folder path.
         2. Folder Path should ends with a "/".
         3. If no folder is specified, it returns the top-level english in
            the bucket.
        ========================================================================
        """
        prefix = folder if folder else str()
        iterator = self._bucket.list_blobs(prefix=prefix,
                                           delimiter='/',
                                           include_trailing_delimiter=True)
        prefixes = set()
        for page in iterator.pages:
            if page.prefixes:
                for p in page.prefixes:
                    trimmed_prefix = p[len(prefix):]
                    if trimmed_prefix:
                        top_level_folder = trimmed_prefix.split('/')[0]
                        prefixes.add(top_level_folder)
        folders = [f'{prefix}{folder}' for folder in
                   prefixes] if folder else list(prefixes)
        return folders

    def files(self, folder: str = None) -> list[str]:
        """
        ========================================================================
         1. Return a list of files within a specified folder path.
         2. Folder Path should ends with a "/" if specified.
         3. If no folder is specified, it returns the files in the root of the
            bucket.
        ========================================================================
        """
        prefix = folder if folder else ''
        iterator = self._bucket.list_blobs(prefix=prefix, delimiter='/')
        files = []
        for blob in iterator:
            if not blob.name.endswith('/'):  # Exclude directories
                trimmed_name = blob.name[len(prefix):]
                if trimmed_name:  # Ensure the file is in the folder
                    files.append(trimmed_name)
        return files

    def upload_file(self,
                    path_from: str,         # Full-Path of the File on the PC
                    path_to: str = None    # Path and File-Name on Storage
                    ) -> None:
        """
        ========================================================================
         Upload File from PC into Google-Storage Bucket.
        ========================================================================
        """
        if not path_to:
            # Upload to the Bucket root-level
            path_to = u_file.to_filename(path_file=path_from)
        blob = self._bucket.blob(blob_name=path_to)
        with open(file=path_from, mode='rb') as file_obj:
            blob.upload_from_file(file_obj=file_obj, retry=Retry())
        if self._verbose:
            print(f'{path_from} uploaded to {path_to}')

    def upload_folder(self,
                      folder_from: str,
                      folder_to: str) -> None:
        """
        ========================================================================
         1. Upload Folder from a PC into Google-Storage.
         2. It remains the folder hierarchy from the PC.
        ========================================================================
        """
        def gen_paths_to(folder_from: str, folder_to: str) -> list[str]:
            folder_to = Blob.to_folder_format(name=folder_to)
            paths_rel = [path.replace('\\', '/') for path in
                         u_folder.filepaths_without_common(folder=folder_from)]
            return [f'{folder_to}{path_rel}' for path_rel in paths_rel]
        paths_from = u_folder.filepaths(folder=folder_from)
        paths_to = gen_paths_to(folder_from=folder_from, folder_to=folder_to)
        for path_from, path_to in zip(paths_from, paths_to):
            self.upload_file(path_from=path_from,
                             path_to=path_to)

    def delete_file(self, path: str) -> None:
        """
        ========================================================================
         Delete a File from a Google-Storage Bucket (by FilePath).
        ========================================================================
        """
        blob = self._bucket.blob(blob_name=path)
        blob.delete()
        if self._verbose:
            print(f'{path} was deleted.')

    def delete_folder(self, path: str) -> None:
        """
        ========================================================================
         Delete all Blobs in the given Folder (by path).
        ========================================================================
        """
        blobs = self._bucket.list_blobs(prefix=path)
        for blob in blobs:
            self.delete_file(path=blob.name)
        