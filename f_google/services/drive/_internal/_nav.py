_FOLDER = 'application/vnd.google-apps.folder'


class _Nav:
    """
    ========================================================================
     Drive Path Navigation — resolve, find, and list.
    ========================================================================
    """

    def __init__(self, service) -> None:
        """
        ====================================================================
         Init with a Google Drive API v3 service object.
        ====================================================================
        """
        self._service = service

    def folders(self, path: str = None) -> list[str]:
        """
        ====================================================================
         Return names of sub-folders at the given path.
        ====================================================================
        """
        parent_id = self.resolve(path=path)
        return self.list_children(parent_id=parent_id,
                                  mime_type=_FOLDER)

    def files(self, path: str = None) -> list[str]:
        """
        ====================================================================
         Return names of files (non-folders) at the given path.
        ====================================================================
        """
        parent_id = self.resolve(path=path)
        return self.list_children(parent_id=parent_id,
                                  mime_type_exclude=_FOLDER)

    def is_exists(self, path: str) -> bool:
        """
        ====================================================================
         Return True if a file or folder exists at the given path.
        ====================================================================
        """
        try:
            self.resolve(path=path)
            return True
        except FileNotFoundError:
            return False

    def resolve(self, path: str = None) -> str:
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
            child_id = self.find_child(parent_id=current_id,
                                       name=part)
            if child_id is None:
                raise FileNotFoundError(
                    f"'{part}' not found in path '{path}'"
                )
            current_id = child_id
        return current_id

    def find_child(self,
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

    def list_children(self,
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
