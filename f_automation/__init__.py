from typing import TYPE_CHECKING

from f_core.imports import ULazy

if TYPE_CHECKING:
    from f_automation.open_sessions import OpenSessions

ULazy.install(globals(), {'OpenSessions': 'f_automation.open_sessions:OpenSessions'})
