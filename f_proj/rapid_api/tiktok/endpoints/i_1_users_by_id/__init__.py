from typing import TYPE_CHECKING

from f_core.imports import ULazy

if TYPE_CHECKING:
    from .main import EndpointUsersById

ULazy.install(globals(), {'EndpointUsersById': '.main:EndpointUsersById'})
