import re


def extract_tels(text: str) -> list[str]:
    """
    ============================================================================
     Return List of Tels extracted from a given Text.
    ============================================================================
    """
    pattern = r'\b9725\d{8}\b'
    return re.findall(pattern=pattern, string=text)
