from google.cloud.storage.bucket import Bucket as GBucket
from f_google.strategies.retry import Retry
from f_google.storage.blob import Blob
from f_os import u_file, u_folder


class Bucket:
    """
    ============================================================================
     Google-Storage Bucket.
    ============================================================================
    """

    def __init__(self, bucket: GBucket) -> None:
        self._bucket: GBucket = bucket

    def folders(self) -> list[str]:
        """
        ========================================================================
         Return List of all Main-Folders in the Bucket.
        ========================================================================
        """
        pages = self._bucket.list_blobs(delimiter='/').pages
        prefixes = set()
        for page in pages:
            prefixes.update(page.prefixes)
        return list(prefixes)

    def files(self, folder: str = None) -> list[str]:
        folder = Blob.to_folder_format(name=folder)
        blobs = self._bucket.list_blobs(prefix=folder, delimiter='/')
        file_paths = [blob.name
                      for blob
                      in blobs
                      if not Blob.is_folder(name=blob.name)]
        return file_paths

    def upload_file(self,
                    path_from: str,         # Full-Path of the File on the PC
                    path_to: str = None,    # Path and File-Name on Storage
                    verbose: bool = True
                    ) -> None:
        """
        ========================================================================
         Upload File from PC into Google-Storage Bucket.
        ========================================================================
        """
        if not path_to:
            # Upload to the Bucket outside the Folders
            path_to = u_file.to_filename(path_file=path_from)
        blob = self._bucket.blob(blob_name=path_to)
        with open(file=path_from, mode='rb') as file_obj:
            blob.upload_from_file(file_obj=file_obj, retry=Retry())
        if verbose:
            print(f'{path_from} uploaded to {path_to}')

    def upload_files(self,
                     paths_from: list[str],
                     path_to: str,
                     verbose: bool = True) -> None:
        """
        ========================================================================
         Upload Files from PC into Google-Storage Bucket.
        ========================================================================
        """
        for path_from in paths_from:
            self.upload_file(path_from=path_from,
                             path_to=path_to,
                             verbose=verbose)

    def upload_folder(self,
                      path_from: str,
                      path_to: str,
                      verbose: bool = True) -> None:
        paths_from = u_folder.filepaths(folder=path_from)
        paths_to = u_folder.filepaths_without_common()