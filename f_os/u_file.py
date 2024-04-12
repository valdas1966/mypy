import os


def to_filename(path_file: str) -> str:
    """
    ============================================================================
     Extract File-Name from the full File-Path.
    ============================================================================
    """
    return path_file.split('\\')[-1]

def to_drive(path_file: str) -> str:
    """
    ============================================================================
     Return the Drive where the given File is stored on.
    ============================================================================
    """
    current = os.path.realpath(path_file)
    drive, _ = os.path.splitdrive(current)
    return drive[0]
