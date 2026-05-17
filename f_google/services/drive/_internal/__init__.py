from f_core.imports import ULazy

ULazy.install(globals(), {
    '_Nav': 'f_google.services.drive._internal._nav:_Nav',
    '_Folders': 'f_google.services.drive._internal._folders:_Folders',
    '_Download': 'f_google.services.drive._internal._download:_Download',
    '_Upload': 'f_google.services.drive._internal._upload:_Upload',
    '_Read': 'f_google.services.drive._internal._read:_Read',
    '_ReadResponse': 'f_google.services.drive._internal._read_response:_ReadResponse',
})
