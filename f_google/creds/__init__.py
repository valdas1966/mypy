from f_core.imports import ULazy

ULazy.install(globals(), {
    'Auth': 'f_google.creds.auth:Auth',
    'OAuth': 'f_google.creds.oauth:OAuth',
})
