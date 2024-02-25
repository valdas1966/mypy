
def to_filename(path_file: str) -> str:
    """
    ============================================================================
     Extract File-Name from the full File-Path.
    ============================================================================
    """
    return path_file.split('\\')[-1]
