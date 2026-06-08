import json
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
         Text must be pure ASCII — see Encoding Note in CLAUDE.md.
        ====================================================================
        """
        bad = sorted({c for c in text if ord(c) > 127})
        if bad:
            raise ValueError(
                f"Non-ASCII chars not supported by Overleaf upload "
                f"(see CLAUDE.md): {bad[:10]}"
            )
        root = self._root()
        parent, name = self._parent_and_name(root=root,
                                             path=path)
        self._delete_child(parent=parent,
                           name=name,
                           kind=pyoverleaf.ProjectFile)
        self._api.project_upload_file(self._key,
                                      parent.id,
                                      name,
                                      text.encode('ascii'))

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

    def set_root_doc(self, name: str) -> None:
        """
        ====================================================================
         Set the Project's compile root document to the named file.
         The file must exist at the project root and be of type 'doc'.
        ====================================================================
        """
        root = self._root()
        for child in root.children:
            if (child.name == name
                    and isinstance(child, pyoverleaf.ProjectFile)
                    and getattr(child, 'type', None) == 'doc'):
                host = self._api._host
                session = self._api._get_session()
                resp = session.post(
                    f'https://{host}/project/{self._key}/settings',
                    json={'rootDocId': child.id},
                    headers={
                        'x-csrf-token':
                            self._api._get_csrf_token(self._key),
                        'Accept': 'application/json',
                    },
                    **self._api._request_kwargs,
                )
                resp.raise_for_status()
                return
        raise ValueError(
            f"No editable doc named '{name}' at project root.")

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

         Reimplements `pyoverleaf.Api.project_get_files`: open the
         project's realtime socket.io connection, read the
         `joinProjectResponse` (which carries the file tree), and
         ALWAYS close the socket in `finally`. The upstream method
         NEVER closes its socket, so each call leaked an open
         realtime connection that Overleaf counts as an online
         'me' collaborator -- and `_root` is hit once per file
         op, so a single push spawned dozens of phantom viewers.
         Closing at the source keeps at most one transient socket
         open at a time and leaves none behind.
        ====================================================================
        """
        socket = self._api._open_socket(self._key)
        try:
            while True:
                line = socket.recv()
                if line.startswith('7:'):
                    raise RuntimeError('Could not get project files.')
                if line.startswith('5:'):
                    break
            data = json.loads(line[len('5:'):].lstrip(':'))
            assert data['name'] == 'joinProjectResponse'
            folders = data['args'][0]['project']['rootFolder']
            return pyoverleaf.ProjectFolder.from_data(folders[0])
        finally:
            try:
                socket.close()
            except Exception:
                pass

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
