from f_core.mixins.has.key import HasKey
from typing import Generic, TypeVar

Key = TypeVar('Key')


class StateBase(Generic[Key], HasKey[Key]):
    """
    ============================================================================
     Configuration in a Search-Space.
    ============================================================================
    """

    def __init__(self, key: Key) -> None:
        """
        ========================================================================
         Init private Attributes.
        ========================================================================
        """
        HasKey.__init__(self, key=key)

    def event_key(self) -> object:
        """
        ========================================================================
         Canonical comparable representation of this State's
         identity, used by recording-test normalizers to produce
         schema-stable event dicts (golden-reference
         comparisons).

         Default returns `self.key`. Override when the key isn't
         trivially comparable / readable in test output (e.g.,
         `StateCell` wraps a `CellMap` → unwraps to a
         `(row, col)` tuple).
        ========================================================================
        """
        return self.key
