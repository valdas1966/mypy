import pyoverleaf
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
