
def from_list(lines: list[str], path: str) -> None:
    """
    ========================================================================
     Convert a list of strings to a text file.
    ========================================================================
    """
    with open(path, 'w') as file:
        for line in lines:
            file.write(line + '\n')


def to_list(path: str) -> list[str]:
    """
    ========================================================================
     Convert a text file to a list of strings without the newlines.
    ========================================================================
    """
    with open(path, 'r') as file:
        lines = file.readlines()
        return [line.strip() for line in lines]
