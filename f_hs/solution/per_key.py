from collections.abc import Mapping
from typing import Generic, TypeVar

from f_cs.solution import SolutionAlgo

Key = TypeVar('Key')
Val = TypeVar('Val')


class SolutionPerKey(SolutionAlgo, Mapping, Generic[Key, Val]):
    """
    ============================================================================
     Per-key Solution wrapper — shared spine for the multi-Solution
     family (SolutionOMSPP, SolutionMOSPP, future SolutionMMSPP).

     Wraps a `dict[Key, Val]` where Val is itself a SolutionAlgo
     (a leaf SolutionSPP, or a nested per-key wrapper). Behaves
     as a `collections.abc.Mapping` over the dict — `.keys()`,
     `.values()`, `.items()`, `__getitem__`, `__iter__`,
     `__len__`, `__contains__`, `.get()`, `==` against other
     Mappings all work.

     `is_valid` is True iff the wrapper is non-empty (the
     producing algorithm guarantees one entry per requested key,
     so non-empty ⇔ "the algorithm completed and attempted every
     key"). The stronger predicate is `is_all_reached`: it
     returns True iff every Val is "reached" — recursing via
     `Val.is_all_reached` when Val is itself a per-key wrapper,
     falling back to `bool(val)` (i.e., Val's own `is_valid`)
     when Val is a leaf SolutionSPP.

     Concrete subclasses pin Key / Val and add a domain alias
     for `_per_key`:
       SolutionOMSPP : Key=goal-State,  Val=SolutionSPP   (per_goal)
       SolutionMOSPP : Key=start-State, Val=SolutionSPP   (per_start)
       SolutionMMSPP : Key=start-State, Val=SolutionOMSPP (per_start)

     MRO: `SolutionAlgo` (Validatable) wins over Mapping for
     `__bool__` — `bool(sol) == sol.is_valid`, NOT
     `len(sol) > 0`. The two happen to agree under this
     constructor (is_valid = bool(per_key) = (len > 0)) but the
     contract is the validity flag, not the len.
    ============================================================================
    """

    def __init__(self, per_key: dict[Key, Val]) -> None:
        """
        ========================================================================
         Init private Attributes.
        ========================================================================
        """
        SolutionAlgo.__init__(self, is_valid=bool(per_key))
        self._per_key: dict[Key, Val] = dict(per_key)

    # ── Mapping protocol ────────────────────────────────

    def __getitem__(self, key: Key) -> Val:
        return self._per_key[key]

    def __iter__(self):
        return iter(self._per_key)

    def __len__(self) -> int:
        return len(self._per_key)

    # ── Public properties ───────────────────────────────

    @property
    def is_all_reached(self) -> bool:
        """
        ========================================================================
         True iff every Val is "reached".

         Recurses into nested per-key wrappers via their own
         `is_all_reached`; falls back to `bool(val)` (= Val's
         `is_valid`) for leaf SolutionSPP values, where
         `is_valid` is True iff `cost < inf`.
        ========================================================================
        """
        return all(
            getattr(v, 'is_all_reached', bool(v))
            for v in self._per_key.values()
        )
