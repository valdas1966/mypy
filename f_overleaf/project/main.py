import pyoverleaf
from pathlib import Path
from f_core.mixins.has.key import HasKey
from f_core.mixins.has.name import HasName


class ProjectOverLeaf(HasName, HasKey[str]):
    """
    ========================================================================
     OverLeaf Project with Key (ID) and Name.
    ========================================================================
    """

    def __init__(self,
                 key: str,
                 name: str,
                 api: pyoverleaf.Api) -> None:
        """
        ====================================================================
         Init private Attributes.
        ====================================================================
        """
        HasKey.__init__(self, key=key)
        HasName.__init__(self, name=name)
        self._api = api

    def list_files(self) -> list[str]:
        """
        ====================================================================
         Return top-level file names.
        ====================================================================
        """
        return [c.name for c in self._root().children
                if isinstance(c, pyoverleaf.ProjectFile)]

    def list_folders(self) -> list[str]:
        """
        ====================================================================
         Return top-level folder names.
        ====================================================================
        """
        return [c.name for c in self._root().children
                if isinstance(c, pyoverleaf.ProjectFolder)]

    def create_folder(self, path: str) -> None:
        """
        ====================================================================
         Create a folder at the given path. Override if exists.
        ====================================================================
        """
        root = self._root()
        parent, name = self._parent_and_name(root=root,
                                             path=path)
        self._delete_child(parent=parent,
                           name=name,
                           kind=pyoverleaf.ProjectFolder)
        self._api.project_create_folder(self._key,
                                        parent.id,
                                        name)

    def delete_folder(self, path: str) -> None:
        """
        ====================================================================
         Delete a folder at the given path. Ignore if not found.
        ====================================================================
        """
        folder = self._find_in(root=self._root(), path=path)
        if folder is None:
            return
        self._api.project_delete_entity(self._key, folder)

    def create_file(self, path: str, text: str) -> None:
        """
        ====================================================================
         Create a text file at the given path. Override if exists.
        ====================================================================
        """
        root = self._root()
        parent, name = self._parent_and_name(root=root,
                                             path=path)
        self._delete_child(parent=parent,
                           name=name,
                           kind=pyoverleaf.ProjectFile)
        self._api.project_upload_file(self._key,
                                      parent.id,
                                      name,
                                      text.encode('utf-8'))

    def upload_file(self,
                    path_src: str,
                    path_dest: str) -> None:
        """
        ====================================================================
         Upload a local file to the given path. Override if exists.
        ====================================================================
        """
        content = Path(path_src).read_bytes()
        root = self._root()
        parent, name = self._parent_and_name(root=root,
                                             path=path_dest)
        self._delete_child(parent=parent,
                           name=name,
                           kind=pyoverleaf.ProjectFile)
        self._api.project_upload_file(self._key,
                                      parent.id,
                                      name,
                                      content)

    def delete_file(self, path: str) -> None:
        """
        ====================================================================
         Delete a file at the given path. Ignore if not found.
        ====================================================================
        """
        root = self._root()
        parent, name = self._parent_and_name(root=root,
                                             path=path)
        for child in parent.children:
            if (child.name == name
                    and isinstance(child,
                                   pyoverleaf.ProjectFile)):
                self._api.project_delete_entity(self._key,
                                                child)
                return

    def _root(self) -> pyoverleaf.ProjectFolder:
        """
        ====================================================================
         Return the root folder of the project.
        ====================================================================
        """
        return self._api.project_get_files(project_id=self._key)

    def _find_in(self,
                 root: pyoverleaf.ProjectFolder,
                 path: str) -> pyoverleaf.ProjectFolder | None:
        """
        ====================================================================
         Find a folder by path within a given root.
        ====================================================================
        """
        parts = path.split('/')
        current = root
        for part in parts:
            found = None
            for child in current.children:
                if (child.name == part
                        and isinstance(child,
                                       pyoverleaf.ProjectFolder)):
                    found = child
                    break
            if found is None:
                return None
            current = found
        return current

    def _parent_and_name(self,
                         root: pyoverleaf.ProjectFolder,
                         path: str
                         ) -> tuple[pyoverleaf.ProjectFolder,
                                    str]:
        """
        ====================================================================
         Split path into parent folder and entity name.
        ====================================================================
        """
        parts = path.rsplit('/', 1)
        if len(parts) == 1:
            return root, parts[0]
        parent = self._find_in(root=root, path=parts[0])
        if parent is None:
            raise ValueError(f'Parent not found: {parts[0]}')
        return parent, parts[1]

    def _delete_child(self,
                      parent: pyoverleaf.ProjectFolder,
                      name: str,
                      kind: type) -> None:
        """
        ====================================================================
         Delete a child entity by name and type if it exists.
        ====================================================================
        """
        for child in parent.children:
            if child.name == name and isinstance(child, kind):
                self._api.project_delete_entity(self._key,
                                                child)
                return
