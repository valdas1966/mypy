import io
import os
from google.oauth2.credentials import Credentials as OAuthCredentials
from google.oauth2.service_account import Credentials as SACredentials
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload, MediaIoBaseDownload


class Drive:
    """
    ========================================================================
     Google Drive Service Wrapper.
    ========================================================================
    """

    # Factory
    Factory: type = None

    _FOLDER = 'application/vnd.google-apps.folder'

    _EXPORT_MIMES = {
        'application/vnd.google-apps.document':
            ('application/pdf', '.pdf'),
        'application/vnd.google-apps.spreadsheet':
            ('application/vnd.openxmlformats-officedocument'
             '.spreadsheetml.sheet', '.xlsx'),
        'application/vnd.google-apps.presentation':
            ('application/pdf', '.pdf'),
        'application/vnd.google-apps.drawing':
            ('application/pdf', '.pdf'),
    }

    def __init__(self,
                 creds: OAuthCredentials | SACredentials) -> None:
        """
        ====================================================================
         Init Drive Client with OAuth or Service-Account Credentials.
        ====================================================================
        """
        self._service = build('drive', 'v3', credentials=creds)

    def folders(self, path: str = None) -> list[str]:
        """
        ====================================================================
         Return names of sub-folders at the given path.
        ====================================================================
        """
        parent_id = self._resolve(path=path)
        return self._list_children(parent_id=parent_id,
                                   mime_type=self._FOLDER)

    def files(self, path: str = None) -> list[str]:
        """
        ====================================================================
         Return names of files (non-folders) at the given path.
        ====================================================================
        """
        parent_id = self._resolve(path=path)
        return self._list_children(parent_id=parent_id,
                                   mime_type_exclude=self._FOLDER)

    def is_exists(self, path: str) -> bool:
        """
        ====================================================================
         Return True if a file or folder exists at the given path.
        ====================================================================
        """
        try:
            self._resolve(path=path)
            return True
        except FileNotFoundError:
            return False

    def delete(self, path: str) -> None:
        """
        ====================================================================
         Permanently delete a file or folder (recursive) at the path.
        ====================================================================
        """
        file_id = self._resolve(path=path)
        self._service.files().delete(fileId=file_id).execute()

    def create_folder(self, path: str) -> None:
        """
        ====================================================================
         Create a folder at the given path.
         Creates intermediate folders if needed (mkdir -p behavior).
         If folder already exists, deletes and re-creates it.
        ====================================================================
        """
        parts = path.strip('/').split('/')
        current_id = 'root'
        for i, part in enumerate(parts):
            child_id = self._find_child(parent_id=current_id,
                                        name=part)
            if child_id is not None:
                # Last segment exists -> delete and re-create
                if i == len(parts) - 1:
                    self._service.files().delete(
                        fileId=child_id
                    ).execute()
                    current_id = self._create_single_folder(
                        parent_id=current_id,
                        name=part
                    )
                else:
                    current_id = child_id
            else:
                current_id = self._create_single_folder(
                    parent_id=current_id,
                    name=part
                )

    def download(self,
                 path_src: str,
                 path_dest: str) -> None:
        """
        ====================================================================
         Download a file or folder from Drive to a local path.
         Creates parent directories locally if needed.
         Google-native docs are exported to suitable formats.
        ====================================================================
        """
        file_id = self._resolve(path=path_src)
        meta = self._service.files().get(
            fileId=file_id,
            fields='mimeType'
        ).execute()
        mime = meta['mimeType']
        if mime == self._FOLDER:
            self._download_folder(folder_id=file_id,
                                  path_local=path_dest)
        else:
            os.makedirs(os.path.dirname(path_dest), exist_ok=True)
            self._download_file(file_id=file_id,
                                mime=mime,
                                path_local=path_dest)

    def upload(self,
               path_src: str,
               path_dest: str) -> None:
        """
        ====================================================================
         Upload a local file or folder to Drive at the given path.
         Creates parent folders on Drive if needed.
         Overwrites silently if a file already exists.
        ====================================================================
        """
        parts = path_dest.strip('/').split('/')
        # Ensure parent folders exist on Drive
        parent_id = self._ensure_parents(parts=parts[:-1])
        name = parts[-1]
        if os.path.isdir(path_src):
            self._upload_folder(path_local=path_src,
                                parent_id=parent_id,
                                name=name)
        else:
            self._upload_file(path_local=path_src,
                              parent_id=parent_id,
                              name=name)

    def _download_file(self,
                       file_id: str,
                       mime: str,
                       path_local: str) -> None:
        """
        ====================================================================
         Download a single file from Drive. Export if Google-native.
        ====================================================================
        """
        if mime in self._EXPORT_MIMES:
            export_mime, ext = self._EXPORT_MIMES[mime]
            # Append export extension if not already present
            if not path_local.endswith(ext):
                path_local += ext
            request = self._service.files().export_media(
                fileId=file_id,
                mimeType=export_mime
            )
        else:
            request = self._service.files().get_media(
                fileId=file_id
            )
        fh = io.FileIO(path_local, 'wb')
        downloader = MediaIoBaseDownload(fh, request)
        done = False
        while not done:
            _, done = downloader.next_chunk()
        fh.close()

    def _download_folder(self,
                         folder_id: str,
                         path_local: str) -> None:
        """
        ====================================================================
         Recursively download a folder from Drive to a local path.
        ====================================================================
        """
        os.makedirs(path_local, exist_ok=True)
        query = (f"'{folder_id}' in parents and "
                 f"trashed = false")
        response = self._service.files().list(
            q=query,
            fields='files(id, name, mimeType)'
        ).execute()
        for item in response.get('files', []):
            child_path = os.path.join(path_local, item['name'])
            if item['mimeType'] == self._FOLDER:
                self._download_folder(folder_id=item['id'],
                                      path_local=child_path)
            else:
                self._download_file(file_id=item['id'],
                                    mime=item['mimeType'],
                                    path_local=child_path)

    def _upload_file(self,
                     path_local: str,
                     parent_id: str,
                     name: str) -> None:
        """
        ====================================================================
         Upload a single file to Drive. Overwrites if exists.
        ====================================================================
        """
        # Check if file already exists
        child_id = self._find_child(parent_id=parent_id,
                                    name=name)
        media = MediaFileUpload(path_local)
        if child_id is not None:
            self._service.files().update(
                fileId=child_id,
                media_body=media
            ).execute()
        else:
            body = {'name': name, 'parents': [parent_id]}
            self._service.files().create(
                body=body,
                media_body=media
            ).execute()

    def _upload_folder(self,
                       path_local: str,
                       parent_id: str,
                       name: str) -> None:
        """
        ====================================================================
         Recursively upload a local folder to Drive.
        ====================================================================
        """
        # Create or overwrite the folder on Drive
        child_id = self._find_child(parent_id=parent_id,
                                    name=name)
        if child_id is not None:
            self._service.files().delete(
                fileId=child_id
            ).execute()
        folder_id = self._create_single_folder(
            parent_id=parent_id,
            name=name
        )
        for entry in os.listdir(path_local):
            entry_path = os.path.join(path_local, entry)
            if os.path.isdir(entry_path):
                self._upload_folder(path_local=entry_path,
                                    parent_id=folder_id,
                                    name=entry)
            else:
                self._upload_file(path_local=entry_path,
                                  parent_id=folder_id,
                                  name=entry)

    def _ensure_parents(self, parts: list[str]) -> str:
        """
        ====================================================================
         Ensure all parent folders exist on Drive (mkdir -p).
         Returns the ID of the deepest parent.
        ====================================================================
        """
        current_id = 'root'
        for part in parts:
            child_id = self._find_child(parent_id=current_id,
                                        name=part)
            if child_id is not None:
                current_id = child_id
            else:
                current_id = self._create_single_folder(
                    parent_id=current_id,
                    name=part
                )
        return current_id

    def _resolve(self, path: str = None) -> str:
        """
        ====================================================================
         Resolve a path string to a Drive file/folder ID.
         None -> 'root' (My Drive root).
        ====================================================================
        """
        if path is None:
            return 'root'
        parts = path.strip('/').split('/')
        current_id = 'root'
        for part in parts:
            child_id = self._find_child(parent_id=current_id,
                                        name=part)
            if child_id is None:
                raise FileNotFoundError(
                    f"'{part}' not found in path '{path}'"
                )
            current_id = child_id
        return current_id

    def _find_child(self,
                    parent_id: str,
                    name: str) -> str | None:
        """
        ====================================================================
         Find a child by name in a parent folder.
         Returns the child's ID, or None if not found.
         Raises ValueError if duplicate names exist.
        ====================================================================
        """
        query = (f"name = '{name}' and "
                 f"'{parent_id}' in parents and "
                 f"trashed = false")
        response = self._service.files().list(
            q=query,
            fields='files(id, name)'
        ).execute()
        files = response.get('files', [])
        if len(files) == 0:
            return None
        if len(files) > 1:
            raise ValueError(
                f"Duplicate name '{name}' in the same folder"
            )
        return files[0]['id']

    def _list_children(self,
                       parent_id: str,
                       mime_type: str = None,
                       mime_type_exclude: str = None
                       ) -> list[str]:
        """
        ====================================================================
         List names of children in a folder.
         Optionally filter by MIME type (include or exclude).
        ====================================================================
        """
        query = (f"'{parent_id}' in parents and "
                 f"trashed = false")
        if mime_type:
            query += f" and mimeType = '{mime_type}'"
        if mime_type_exclude:
            query += f" and mimeType != '{mime_type_exclude}'"
        response = self._service.files().list(
            q=query,
            fields='files(name)'
        ).execute()
        return [f['name'] for f in response.get('files', [])]

    def _create_single_folder(self,
                              parent_id: str,
                              name: str) -> str:
        """
        ====================================================================
         Create a single folder and return its ID.
        ====================================================================
        """
        body = {
            'name': name,
            'mimeType': self._FOLDER,
            'parents': [parent_id]
        }
        folder = self._service.files().create(
            body=body,
            fields='id'
        ).execute()
        return folder['id']
