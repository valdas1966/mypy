import fitz
import pymupdf4llm
from f_pdf.response.main import ResponsePdf


class UPdf:
    """
    ========================================================================
     Static PDF Utility — parses PDF bytes into text and page images.
    ========================================================================
    """

    @staticmethod
    def read(data: bytes, dpi: int = 200) -> ResponsePdf:
        """
        ====================================================================
         Parse PDF bytes into markdown text and rendered page images.
         Uses pymupdf4llm for text/table extraction and PyMuPDF for
         page rendering.
        ====================================================================
        """
        doc = fitz.open(stream=data, filetype='pdf')
        # Extract markdown (text + tables)
        text = pymupdf4llm.to_markdown(doc)
        # Render each page as PNG
        pages = []
        for page in doc:
            pixmap = page.get_pixmap(dpi=dpi)
            pages.append(pixmap.tobytes('png'))
        doc.close()
        return ResponsePdf(text=text, pages=pages)
