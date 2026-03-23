class _ReadResponse:
    """
    ========================================================================
     Response from Drive.read() — file content read into memory.
    ========================================================================
    """

    def __init__(self,
                 text: str,
                 pages: list[bytes] = None) -> None:
        """
        ====================================================================
         Init with text content and optional page images.
        ====================================================================
        """
        self._text = text
        self._pages = pages if pages is not None else []

    @property
    def text(self) -> str:
        """
        ====================================================================
         Return the text content (decoded string or PDF markdown).
        ====================================================================
        """
        return self._text

    @property
    def pages(self) -> list[bytes]:
        """
        ====================================================================
         Return rendered page images as PNG bytes (PDF only).
        ====================================================================
        """
        return self._pages

    def __str__(self) -> str:
        """
        ====================================================================
         Return the text content.
        ====================================================================
        """
        return self._text

    def __repr__(self) -> str:
        """
        ====================================================================
         Return a debug representation.
        ====================================================================
        """
        return (f'ReadResponse(chars={len(self._text)}, '
                f'pages={len(self._pages)})')
