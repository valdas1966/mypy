from typing import TYPE_CHECKING

from f_core.imports import ULazy

if TYPE_CHECKING:
    from .main import EndpointHashtagsByKeyword

ULazy.install(globals(), {'EndpointHashtagsByKeyword': '.main:EndpointHashtagsByKeyword'})
