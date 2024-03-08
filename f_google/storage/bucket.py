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
        prefixes = {page.prefixes for page in pages}
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

    def upload_folder(self,
                      folder_from: str,
                      folder_to: str,
                      verbose: bool = True) -> None:
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
                             path_to=path_to,
                             verbose=verbose)
