from google.oauth2.credentials import Credentials as OAuthCredentials
from google.oauth2.service_account import Credentials as SACredentials
from googleapiclient.discovery import build


class Drive:
    """
    ========================================================================
     Google Drive Service Wrapper.
    ========================================================================
    """

    # Factory
    Factory: type = None

    _FOLDER = 'application/vnd.google-apps.folder'

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
