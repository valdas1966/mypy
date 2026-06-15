from typing import TYPE_CHECKING

from f_core.imports import ULazy

if TYPE_CHECKING:
    from f_google.services.drive._internal._nav import _Nav
    from f_google.services.drive._internal._folders import _Folders
    from f_google.services.drive._internal._download import _Download
    from f_google.services.drive._internal._upload import _Upload
    from f_google.services.drive._internal._read import _Read
    from f_google.services.drive._internal._read_response import _ReadResponse
    from f_google.services.drive._internal._serial import _Serial

ULazy.install(globals(), {
    '_Nav': 'f_google.services.drive._internal._nav:_Nav',
    '_Folders': 'f_google.services.drive._internal._folders:_Folders',
    '_Download': 'f_google.services.drive._internal._download:_Download',
    '_Upload': 'f_google.services.drive._internal._upload:_Upload',
    '_Read': 'f_google.services.drive._internal._read:_Read',
    '_ReadResponse': 'f_google.services.drive._internal._read_response:_ReadResponse',
    '_Serial': 'f_google.services.drive._internal._serial:_Serial',
})
