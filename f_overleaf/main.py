import json
import pyoverleaf
from bs4 import BeautifulSoup
from f_core.mixins.dictable import Dictable
from f_overleaf.project.main import ProjectOverLeaf


class OverLeaf(Dictable[str, ProjectOverLeaf]):
    """
    ========================================================================
     OverLeaf Service Wrapper.
    ========================================================================
    """

    # Factory
    Factory: type = None

    def __init__(self, api: pyoverleaf.Api) -> None:
        """
        ====================================================================
         Init OverLeaf Client with an authenticated Api instance.
        ====================================================================
        """
        self._api = api
        projects = {p.name: ProjectOverLeaf(key=p.id,
                                            name=p.name,
                                            api=self._api)
                    for p in self._api.get_projects()}
        Dictable.__init__(self, data=projects)

    def close(self) -> None:
        """
        ====================================================================
         Explicit teardown hook. pyoverleaf keeps NO long-lived
         connection: every HTTP call builds a throwaway
         `requests.Session`, and the realtime socket.io
         connections are now closed at the source in
         `ProjectOverLeaf._root` (upstream `project_get_files`
         leaked them -> phantom online 'me' collaborators). So
         there is no persistent handle to release here; this hook
         forces a GC sweep to promptly reap any stray socket
         objects and gives callers an explicit close +
         `with`-statement support. Safe + idempotent.
        ====================================================================
        """
        import gc
        gc.collect()

    def __enter__(self) -> 'OverLeaf':
        """
        ====================================================================
         Enter a `with OverLeaf.Factory...() as ol:` block.
        ====================================================================
        """
        return self

    def __exit__(self, *exc: object) -> None:
        """
        ====================================================================
         Close on block exit (success or exception).
        ====================================================================
        """
        self.close()

    def create_project(self, name: str) -> ProjectOverLeaf:
        """
        ====================================================================
         Create a blank OverLeaf Project and return it.
         Raises ValueError if a Project with the same name exists.
        ====================================================================
        """
        if name in self:
            raise ValueError(f"Project '{name}' already exists.")
        host = self._api._host
        session = self._api._get_session()
        resp = session.post(
            f'https://{host}/project/new',
            json={'projectName': name, 'template': 'none'},
            headers={'x-csrf-token': self._csrf()},
            **self._api._request_kwargs,
        )
        resp.raise_for_status()
        pid = resp.json()['project_id']
        project = ProjectOverLeaf(key=pid,
                                  name=name,
                                  api=self._api)
        self[name] = project
        return project

    def delete_project(self, name: str) -> None:
        """
        ====================================================================
         Delete an existing Project. Raises KeyError if missing.
        ====================================================================
        """
        pid = self[name].key
        host = self._api._host
        session = self._api._get_session()
        resp = session.delete(
            f'https://{host}/project/{pid}',
            headers={'x-csrf-token': self._csrf()},
            **self._api._request_kwargs,
        )
        resp.raise_for_status()
        del self._data[name]

    def tag_project(self,
                    project_name: str,
                    tag_name: str) -> None:
        """
        ====================================================================
         Apply a Tag to a Project. Create the Tag if absent.
        ====================================================================
        """
        pid = self[project_name].key
        host = self._api._host
        session = self._api._get_session()
        # One dashboard fetch — pulls CSRF + existing tags
        page = session.get(f'https://{host}/project',
                           **self._api._request_kwargs)
        page.raise_for_status()
        soup = BeautifulSoup(page.content, features='html.parser')
        token = soup.find('meta',
                          dict(name='ol-csrfToken')).get('content')
        tags = json.loads(soup.find(
            'meta', dict(name='ol-tags')).get('content'))
        tid = next((t['_id'] for t in tags
                    if t['name'] == tag_name), None)
        if tid is None:
            # Create the tag
            r = session.post(
                f'https://{host}/tag',
                json={'name': tag_name},
                headers={'x-csrf-token': token,
                         'Accept': 'application/json'},
                **self._api._request_kwargs,
            )
            r.raise_for_status()
            tid = r.json()['_id']
        # Apply tag to project
        r = session.post(
            f'https://{host}/tag/{tid}/project/{pid}',
            headers={'x-csrf-token': token},
            **self._api._request_kwargs,
        )
        r.raise_for_status()

    def _csrf(self) -> str:
        """
        ====================================================================
         Pull a fresh CSRF token from the project dashboard.
        ====================================================================
        """
        host = self._api._host
        session = self._api._get_session()
        r = session.get(f'https://{host}/project',
                        **self._api._request_kwargs)
        r.raise_for_status()
        soup = BeautifulSoup(r.content, features='html.parser')
        return soup.find('meta',
                         dict(name='ol-csrfToken')).get('content')
