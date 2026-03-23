from dataclasses import dataclass


@dataclass
class ResponsePdf:
    """
    ========================================================================
     Parsed PDF Content (text + rendered page images).
    ========================================================================
    """

    text: str
    pages: list[bytes]

    def __repr__(self) -> str:
        """
        ====================================================================
         Return a debug representation.
        ====================================================================
        """
        return (f'ResponsePdf(chars={len(self.text)}, '
                f'pages={len(self.pages)})')
