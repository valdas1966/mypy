from urllib.parse import parse_qs, urlparse


class UUrl:
    """
    ============================================================================
     Static Utility for URL Parsing.
    ============================================================================
    """

    Factory: type = None

    @staticmethod
    def suffix(url: str) -> str | None:
        """
        ====================================================================
         Return the file suffix of the URL (without leading dot).
        ====================================================================
        """
        parsed = urlparse(url)
        # Try to extract suffix from path (filename.ext)
        path = parsed.path
        filename = path.rsplit('/', 1)[-1] if '/' in path else path
        if '.' in filename:
            ext = filename.rsplit('.', 1)[-1].lower()
            if ext:
                return ext
        # Fallback: try mime_type in query params
        qs = parse_qs(parsed.query)
        mime_vals = qs.get('mime_type') or qs.get('mimeType')
        if mime_vals:
            ext = mime_vals[0].lower().split('_')[-1].split('/')[-1]
            if ext:
                return ext
        return None
