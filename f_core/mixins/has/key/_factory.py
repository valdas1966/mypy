from typing import TypeVar

from f_core.mixins.has.key.main import HasKey

K = TypeVar('K')


def create_has_key(key: K) -> HasKey[K]:
    """
    ============================================================================
     Factory function to create HasKey instances.
    ============================================================================
    """
    return HasKey(key)