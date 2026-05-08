"""
============================================================================
 OpenSessions - open Claude Code sessions in OS-native terminal tabs.
============================================================================
"""
from __future__ import annotations

import platform
import re
import sys


_NAME_PATTERN = re.compile(r'^[A-Za-z0-9_][A-Za-z0-9_-]*$')


class OpenSessions:
    """
    ============================================================================
     OpenSessions - opens Claude sessions in native terminal tabs.
    ============================================================================
     Each tab launches `claude` with `start session '<name>';` pre-submitted.
     Routes to the OS-specific backend at runtime (Windows/WSL via wt.exe;
     Mac stub).
    ============================================================================
    """

    Factory: type = None

    def __init__(self,
                 path_project: str = '/mnt/f/mypy') -> None:
        """
        ========================================================================
         Init private Attributes.
        ========================================================================
        """
        self._path_project = path_project

    @property
    def path_project(self) -> str:
        """
        ========================================================================
         Return the Project-Directory path used inside each tab.
        ========================================================================
        """
        return self._path_project

    def open(self,
             names: list[str]) -> None:
        """
        ========================================================================
         Open one terminal-tab per Session-Name.
        ========================================================================
        """
        if not names:
            raise ValueError('names must be non-empty')
        for name in names:
            self._validate_name(name=name)
        os_name = self._detect_os()
        if os_name == 'windows':
            from f_automation.open_sessions._backend_windows import (
                open_windows
            )
            open_windows(names=names,
                         path_project=self._path_project)
        elif os_name == 'mac':
            raise NotImplementedError(
                'Mac backend not yet implemented'
            )
        else:
            raise RuntimeError(
                f'unsupported platform: {os_name}'
            )

    @staticmethod
    def _validate_name(name: str) -> None:
        """
        ========================================================================
         Reject Session-Names with shell-special characters.
        ========================================================================
        """
        if not _NAME_PATTERN.match(name):
            raise ValueError(
                f'invalid session name: {name!r} '
                f"(allowed: [A-Za-z0-9_-], must start with alnum or '_')"
            )

    @staticmethod
    def _detect_os() -> str:
        """
        ========================================================================
         Return 'windows' (incl. WSL), 'mac', or 'linux'.
        ========================================================================
        """
        sysname = platform.system()
        if sysname == 'Darwin':
            return 'mac'
        if sysname == 'Windows':
            return 'windows'
        # Linux: check WSL via /proc/version
        try:
            with open('/proc/version', 'r') as f:
                if 'microsoft' in f.read().lower():
                    return 'windows'
        except FileNotFoundError:
            pass
        return 'linux'

    def __repr__(self) -> str:
        return f'OpenSessions(path_project={self._path_project!r})'


if __name__ == '__main__':
    if len(sys.argv) < 2:
        print(
            'usage: python -m f_automation.open_sessions.main '
            'name1 [name2 ...]'
        )
        sys.exit(1)
    OpenSessions().open(names=sys.argv[1:])
