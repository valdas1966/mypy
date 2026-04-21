from google.oauth2.credentials import Credentials as OAuthCredentials
from google.oauth2.service_account import Credentials as SACredentials
from googleapiclient.discovery import build
from f_google.services.drive._internal import (
    _Nav, _Folders, _Download, _Upload, _Read, _ReadResponse
)


class Drive:
    """
    ========================================================================
     Google Drive Service Wrapper.
    ========================================================================
    """

    # Factory
    Factory: type = None

    def __init__(self,
                 creds: OAuthCredentials | SACredentials) -> None:
        """
        ====================================================================
         Init Drive Client with OAuth or Service-Account Credentials.
        ====================================================================
        """
        service = build('drive', 'v3', credentials=creds)
        self._nav = _Nav(service=service)
        self._folders = _Folders(service=service,
                                 nav=self._nav)
        self._download = _Download(service=service,
                                   nav=self._nav)
        self._upload = _Upload(service=service,
                               nav=self._nav,
                               folders=self._folders)
        self._read = _Read(service=service,
                           nav=self._nav)

    def folders(self, path: str = None) -> list[str]:
        """
        ====================================================================
         Return names of sub-folders at the given path.
        ====================================================================
        """
        return self._nav.folders(path=path)

    def files(self, path: str = None) -> list[str]:
        """
        ====================================================================
         Return names of files (non-folders) at the given path.
        ====================================================================
        """
        return self._nav.files(path=path)

    def is_exists(self, path: str) -> bool:
        """
        ====================================================================
         Return True if a file or folder exists at the given path.
        ====================================================================
        """
        return self._nav.is_exists(path=path)

    def create_folder(self, path: str) -> None:
        """
        ====================================================================
         Create a folder at the given path (mkdir -p).
         If folder already exists, deletes and re-creates it.
        ====================================================================
        """
        self._folders.create(path=path)

    def delete(self, path: str) -> None:
        """
        ====================================================================
         Permanently delete a file or folder (recursive).
        ====================================================================
        """
        self._folders.delete(path=path)

    def download(self,
                 path_src: str,
                 path_dest: str) -> None:
        """
        ====================================================================
         Download a file or folder from Drive to a local path.
        ====================================================================
        """
        self._download.download(path_src=path_src,
                                path_dest=path_dest)

    def upload(self,
               path_src: str,
               path_dest: str) -> None:
        """
        ====================================================================
         Upload a local file or folder to Drive.
        ====================================================================
        """
        self._upload.upload(path_src=path_src,
                            path_dest=path_dest)

    def read(self,
             path: str,
             encoding: str = 'utf-8') -> _ReadResponse:
        """
        ====================================================================
         Read a file from Drive into memory (no disk writes).
        ====================================================================
        """
        return self._read.read(path=path, encoding=encoding)

    def get_path_by_id(self, file_id: str) -> str:
        """
        ====================================================================
         Resolve a Drive file/folder ID to its '/'-joined path relative
         to My Drive root. Raises FileNotFoundError for unknown IDs.
        ====================================================================
        """
        return self._nav.path_of(file_id=file_id)
