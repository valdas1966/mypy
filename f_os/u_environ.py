import os

"""
================================================================================
 Utils Functions for Environment-Variables.
================================================================================
"""


def set(name: str, value: str) -> None:
    """
    ============================================================================
     Set list new Environment-Variable.
    ============================================================================
    """
    os.environ[name] = value


def get(name: str) -> str:
    """
    ============================================================================
     Return the Environment-Variable value.
    ============================================================================
    """
    return os.environ.get(name)


def remove(name: str) -> None:
    """
    ============================================================================
     Remove the Environment-Variable.
    ============================================================================
    """
    os.environ.pop(name)
