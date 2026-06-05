from typing import TYPE_CHECKING

from f_core.imports import ULazy

if TYPE_CHECKING:
    from .main import EndpointVideosByHashtag

ULazy.install(globals(), {'EndpointVideosByHashtag': '.main:EndpointVideosByHashtag'})
