
def get_filename(filepath: str, with_domain: bool = True) -> str:
    """
    ============================================================================
     Description: Return FileName extracted from the FilePath.
    ============================================================================
     Example: with domain [test_1.txt], without [test_1]
    ============================================================================
    """
    ans = filepath.split('\\')[-1]
    if not with_domain:
        ans = ans.split('.')[0]
    return ans


def get_dir(filepath: str) -> str:
    """
    ============================================================================
     Description: Return the Directory-Path of the given File-Path.
    ============================================================================
    """
    return '\\'.join(filepath.split('\\')[:-1])
