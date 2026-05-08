from f_automation.open_sessions.main import OpenSessions


class Factory:
    """
    ============================================================================
     Factory-Class for OpenSessions.
    ============================================================================
    """

    @staticmethod
    def a() -> OpenSessions:
        """
        ========================================================================
         Default OpenSessions for the MyPy project (path_project=/mnt/f/mypy).
        ========================================================================
        """
        return OpenSessions(path_project='/mnt/f/mypy')

    @staticmethod
    def at(path_project: str) -> OpenSessions:
        """
        ========================================================================
         OpenSessions targeting a custom Project-Directory.
        ========================================================================
        """
        return OpenSessions(path_project=path_project)
