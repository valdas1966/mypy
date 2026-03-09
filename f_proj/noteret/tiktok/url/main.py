
from urllib.parse import parse_qs, urlparse


class URL:
    """
    ===========================================================================
     Utils class for URL.
    ===========================================================================
    """
    
    # Factory
    Factory = None
    
    def __init__(self, url: str) -> None:
        """
        =======================================================================
         Init private Attributes.
        =======================================================================
        """
        self._url = url
        
    def suffix(self) -> str | None:
        """
        =======================================================================
         Return the suffix of the url (without leading dot).
        =======================================================================
        """
        parsed = urlparse(self._url)

        # 1) Try to extract suffix from path (filename.ext)
        path = parsed.path
        filename = path.rsplit("/", 1)[-1] if "/" in path else path

        if "." in filename:
            # Take text after last dot
            ext = filename.rsplit(".", 1)[-1].lower()
            if ext:
                return ext   # <- no "."

        # 2) Fallback: try mime_type in query...
        qs = parse_qs(parsed.query)
        mime_vals = qs.get("mime_type") or qs.get("mimeType")

        if mime_vals:
            mime = mime_vals[0].lower()
            ext = mime.split("_")[-1].split("/")[-1]
            if ext:
                return ext   # <- no "."

        return None