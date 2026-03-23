from f_pdf.response.main import ResponsePdf


class Factory:
    """
    ========================================================================
     Factory for ResponsePdf test instances.
    ========================================================================
    """

    @staticmethod
    def gen(text: str = 'Sample PDF text.',
            nr_pages: int = 1) -> ResponsePdf:
        """
        ====================================================================
         Generate a ResponsePdf with given text and empty PNG pages.
        ====================================================================
        """
        pages = [b'PNG' for _ in range(nr_pages)]
        return ResponsePdf(text=text, pages=pages)
