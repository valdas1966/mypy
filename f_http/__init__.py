from typing import TYPE_CHECKING

from f_core.imports import ULazy

if TYPE_CHECKING:
    from .client import Client
    from .status import Status
    from .response import Response

ULazy.install(globals(), {
    'Client': '.client:Client',
    'Status': '.status:Status',
    'Response': '.response:Response',
})
