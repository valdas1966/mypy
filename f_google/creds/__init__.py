from typing import TYPE_CHECKING

from f_core.imports import ULazy

if TYPE_CHECKING:
    from f_google.creds.auth import Auth
    from f_google.creds.oauth import OAuth

ULazy.install(globals(), {
    'Auth': 'f_google.creds.auth:Auth',
    'OAuth': 'f_google.creds.oauth:OAuth',
})
