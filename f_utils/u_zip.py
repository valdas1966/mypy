from zipfile import ZipFile


def files(li, dest):
    """
    ============================================================================
     Description: Zip Multiple Files into Single-Archive.
    ============================================================================
     Arguments:
    ----------------------------------------------------------------------------
        1. li : list of str (List of FilePaths).
        2. dest : str (FilePath of Archive Destination).
    ============================================================================
    """
    z = ZipFile(dest, 'w')
    for f in li:
        z.write(f)
    z.close()
