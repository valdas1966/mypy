import os


def filepaths(folder: str) -> list[str]:
    """
    ============================================================================
     Return List of all FilePaths in the received Folder.
    ============================================================================
    """
    res = list()
    for root, _, files in os.walk(folder):
        for file in files:
            filepath = os.path.join(root, file)
            res.append(filepath)
    return res


def filepaths_without_common(folder: str) -> list[str]:
    """
    ============================================================================
     Return List of FilePaths without their Common-Root.
    ============================================================================
    """
    paths = filepaths(folder=folder)
    root_common = os.path.commonpath(paths)
    return [os.path.relpath(path, root_common)
            for path
            in paths]
