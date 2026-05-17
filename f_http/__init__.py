from f_core.imports import ULazy

ULazy.install(globals(), {
    'Client': '.client:Client',
    'Status': '.status:Status',
    'Response': '.response:Response',
})
