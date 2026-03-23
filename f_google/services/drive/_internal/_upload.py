import os
from googleapiclient.http import MediaFileUpload
from f_google.services.drive._internal._nav import _Nav, _FOLDER
from f_google.services.drive._internal._folders import _Folders


class _Upload:
    """
    ========================================================================
     Drive Upload — upload files/folders from local disk.
    ========================================================================
    """

    def __init__(self,
                 service,
                 nav: _Nav,
                 folders: _Folders) -> None:
        """
        ====================================================================
         Init with a Drive API service, navigation and folders helpers.
        ====================================================================
        """
        self._service = service
        self._nav = nav
        self._folders = folders

    def upload(self,
               path_src: str,
               path_dest: str) -> None:
        """
        ====================================================================
         Upload a local file or folder to Drive.
         Creates parent folders on Drive if needed.
         Overwrites silently if a file already exists.
        ====================================================================
        """
        parts = path_dest.strip('/').split('/')
        # Ensure parent folders exist on Drive
        parent_id = self._folders.ensure_parents(
            parts=parts[:-1]
        )
        name = parts[-1]
        if os.path.isdir(path_src):
            self._folder(path_local=path_src,
                         parent_id=parent_id,
                         name=name)
        else:
            self._file(path_local=path_src,
                       parent_id=parent_id,
                       name=name)

    def _file(self,
              path_local: str,
              parent_id: str,
              name: str) -> None:
        """
        ====================================================================
         Upload a single file. Overwrites if exists.
        ====================================================================
        """
        child_id = self._nav.find_child(parent_id=parent_id,
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

    def _folder(self,
                path_local: str,
                parent_id: str,
                name: str) -> None:
        """
        ====================================================================
         Recursively upload a local folder to Drive.
        ====================================================================
        """
        child_id = self._nav.find_child(parent_id=parent_id,
                                        name=name)
        if child_id is not None:
            self._service.files().delete(
                fileId=child_id
            ).execute()
        folder_id = self._folders._create_single(
            parent_id=parent_id,
            name=name
        )
        for entry in os.listdir(path_local):
            entry_path = os.path.join(path_local, entry)
            if os.path.isdir(entry_path):
                self._folder(path_local=entry_path,
                             parent_id=folder_id,
                             name=entry)
            else:
                self._file(path_local=entry_path,
                           parent_id=folder_id,
                           name=entry)
