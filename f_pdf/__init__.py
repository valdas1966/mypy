from typing import TYPE_CHECKING

from f_core.imports import ULazy

if TYPE_CHECKING:
    from f_pdf.main import UPdf
    from f_pdf.response import ResponsePdf

ULazy.install(globals(), {
    'UPdf': 'f_pdf.main:UPdf',
    'ResponsePdf': 'f_pdf.response:ResponsePdf',
})
