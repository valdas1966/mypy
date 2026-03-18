import pyoverleaf


class Overleaf:
    """
    ========================================================================
     Overleaf Service Wrapper.
    ========================================================================
    """

    # Factory
    Factory: type = None

    def __init__(self, api: pyoverleaf.Api) -> None:
        """
        ====================================================================
         Init Overleaf Client with an authenticated Api instance.
        ====================================================================
        """
        self._api = api

    def projects(self) -> list[str]:
        """
        ====================================================================
         Return names of all projects.
        ====================================================================
        """
        return [p.name for p in self._api.get_projects()]
