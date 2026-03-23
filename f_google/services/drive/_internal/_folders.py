from f_google.services.drive._internal._nav import _Nav, _FOLDER


class _Folders:
    """
    ========================================================================
     Drive Folder Operations — create, delete, ensure parents.
    ========================================================================
    """

    def __init__(self, service, nav: _Nav) -> None:
        """
        ====================================================================
         Init with a Drive API service and navigation helper.
        ====================================================================
        """
        self._service = service
        self._nav = nav

    def create(self, path: str) -> None:
        """
        ====================================================================
         Create a folder at the given path (mkdir -p).
         If folder already exists, deletes and re-creates it.
        ====================================================================
        """
        parts = path.strip('/').split('/')
        current_id = 'root'
        for i, part in enumerate(parts):
            child_id = self._nav.find_child(
                parent_id=current_id,
                name=part
            )
            if child_id is not None:
                # Last segment exists -> delete and re-create
                if i == len(parts) - 1:
                    self._service.files().delete(
                        fileId=child_id
                    ).execute()
                    current_id = self._create_single(
                        parent_id=current_id,
                        name=part
                    )
                else:
                    current_id = child_id
            else:
                current_id = self._create_single(
                    parent_id=current_id,
                    name=part
                )

    def delete(self, path: str) -> None:
        """
        ====================================================================
         Permanently delete a file or folder (recursive).
        ====================================================================
        """
        file_id = self._nav.resolve(path=path)
        self._service.files().delete(fileId=file_id).execute()

    def ensure_parents(self, parts: list[str]) -> str:
        """
        ====================================================================
         Ensure all parent folders exist on Drive (mkdir -p).
         Returns the ID of the deepest parent.
        ====================================================================
        """
        current_id = 'root'
        for part in parts:
            child_id = self._nav.find_child(
                parent_id=current_id,
                name=part
            )
            if child_id is not None:
                current_id = child_id
            else:
                current_id = self._create_single(
                    parent_id=current_id,
                    name=part
                )
        return current_id

    def _create_single(self,
                       parent_id: str,
                       name: str) -> str:
        """
        ====================================================================
         Create a single folder and return its ID.
        ====================================================================
        """
        body = {
            'name': name,
            'mimeType': _FOLDER,
            'parents': [parent_id]
        }
        folder = self._service.files().create(
            body=body,
            fields='id'
        ).execute()
        return folder['id']
