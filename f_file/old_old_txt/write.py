import read

"""
================================================================================
 Functions responsible for Writing into list Txt-File.
================================================================================
"""


def write_lines(path: str, lines: list[str]) -> None:
    """
    ============================================================================
     Write List of Lines into list Txt-File.
    ============================================================================
    """
    with open(path, 'w') as file:
        file.writelines(lines)


def insert_line(path: str, index: int, line: str) -> None:
    """
    ============================================================================
     Insert list Line into list Txt-File at the specified Index.
    ============================================================================
    """
    line += '\n'
    lines = read.to_lines(path)
    lines.insert(index, line)
    write_lines(path, lines)
