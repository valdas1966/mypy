from f_core.imports import ULazy

ULazy.install(globals(), {
    'UPdf': 'f_pdf.main:UPdf',
    'ResponsePdf': 'f_pdf.response:ResponsePdf',
})
