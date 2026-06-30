from collections.abc import Mapping
from typing import Iterator


class Counters(Mapping):
    """
    ============================================================================
     Always-on Operation Counters for Algorithms.

     A small, always-on observability primitive — sibling of
     `Recorder`. Where Recorder captures opt-in structured
     traces, Counters give cheap O(1) per-run summaries that
     stay live during benchmark runs (recording typically off).

     Schema is declared at construction. Names live in a tuple,
     values in an internal dict. Optional `groups` attaches
     blank-line separators to the `__repr__` for visual
     scanning of related counter families.

     Mapping protocol: indexing, iteration, `.items()`,
     `dict(c)`, and `c == {...}` all work — so the dict-like
     consumer surface that callers expect from `algo.counters`
     keeps working when the property returns a Counters
     instance.
    ============================================================================
    """

    # Factory
    Factory: type = None

    def __init__(self,
                 names: (tuple[str, ...]
                         | tuple[tuple[str, ...], ...])
                 ) -> None:
        """
        ====================================================================
         Init private Attributes.

         `names` accepts two forms:
           - flat `tuple[str, ...]` — single un-grouped block.
           - tuple of tuples `tuple[tuple[str, ...], ...]` —
             groups for `__repr__` blank-line separation.
                 Detected by inspecting the first element's type.
        ====================================================================
        """
        # Normalize to tuple-of-tuples for grouping.
        if names and isinstance(names[0], str):
            self._groups: tuple[tuple[str, ...], ...] = (
                tuple(names),)
        else:
            self._groups = tuple(tuple(g) for g in names)
        # Flat name tuple, in declaration order.
        self._names: tuple[str, ...] = tuple(
            n for g in self._groups for n in g)
        # Reject duplicates — schema would be ambiguous.
        if len(set(self._names)) != len(self._names):
            raise ValueError(
                f'duplicate counter names: {self._names}')
        # Values dict (preserves declaration order).
        self._values: dict[str, int] = {
            n: 0 for n in self._names}

    # ──────────────────────────────────────────────────
    #  Mutation
    # ──────────────────────────────────────────────────

    def inc(self, name: str, n: int = 1) -> None:
        """
        ====================================================================
         Increment counter `name` by `n` (default 1).
         Raises `KeyError` if `name` is not declared — catches
         typos at the call site rather than silently spawning
         a phantom counter.
        ====================================================================
        """
        if name not in self._values:
            raise KeyError(
                f'unknown counter {name!r}; '
                f'declared: {self._names}')
        self._values[name] += n

    def reset(self) -> None:
        """
        ====================================================================
         Zero all counters in place.
        ====================================================================
        """
        for n in self._names:
            self._values[n] = 0

    def assign(self, name: str, value: int) -> None:
        """
        ====================================================================
         Set counter `name` to the absolute `value` (overwrites
         any prior count). Use for ownership-handoff: when
         another component owns the value and this Counters
         mirrors the final tally (e.g., an algorithm syncs
         frontier-owned push/pop/decrease counts into its own
         8-counter scaffold at end-of-run).

         Raises `KeyError` on undeclared `name` — same typo
         guard as `inc`.
        ====================================================================
        """
        if name not in self._values:
            raise KeyError(
                f'unknown counter {name!r}; '
                f'declared: {self._names}')
        self._values[name] = value

    def absorb(self,
               source: Mapping,
               names: tuple[str, ...] | None = None,
               default: int = 0) -> None:
        """
        ====================================================================
         Mirror counters from `source` into this Counters by
         absolute assignment. For each name in `names`
         (default: this Counters' full schema), copy
         `source[name]` when present, else write `default`.

         Centralizes the structural-default policy for
         cross-component handoff: an algorithm mirroring a
         frontier's push/pop/decrease tally synthesizes
         `cnt_decrease = 0` for a FIFO frontier that does not
         track it — replacing a per-call-site
         `'cnt_decrease' in fc` guard.

         `source` may be any Mapping (a Counters or a plain
         dict). Each target name must be declared here
         (`KeyError` via `assign`); source-only names are
         ignored.
        ====================================================================
        """
        targets = self._names if names is None else names
        for name in targets:
            value = source[name] if name in source else default
            self.assign(name, value)

    # ──────────────────────────────────────────────────
    #  Snapshot
    # ──────────────────────────────────────────────────

    def as_dict(self) -> dict[str, int]:
        """
        ====================================================================
         Return a plain-dict snapshot in declaration order.
         The returned dict is a copy — mutating it does not
         affect the Counters.
        ====================================================================
        """
        return dict(self._values)

    # ──────────────────────────────────────────────────
    #  Mapping Protocol
    # ──────────────────────────────────────────────────

    def __getitem__(self, name: str) -> int:
        """
        ====================================================================
         Return the current value of counter `name`.
        ====================================================================
        """
        return self._values[name]

    def __iter__(self) -> Iterator[str]:
        """
        ====================================================================
         Iterate counter names in declaration order.
        ====================================================================
        """
        return iter(self._names)

    def __len__(self) -> int:
        """
        ====================================================================
         Number of declared counters.
        ====================================================================
        """
        return len(self._names)

    # ──────────────────────────────────────────────────
    #  Equality
    # ──────────────────────────────────────────────────

    def __eq__(self, other: object) -> bool:
        """
        ====================================================================
         Equal to another Counters with the same name→value
         map, or to any Mapping (incl. plain dict) with the
         same name→value map. Group structure is not part of
         identity.
        ====================================================================
        """
        if isinstance(other, Counters):
            return self._values == other._values
        if isinstance(other, Mapping):
            return self._values == dict(other)
        return NotImplemented

    # Mutable container — explicitly unhashable.
    __hash__ = None

    # ──────────────────────────────────────────────────
    #  Repr
    # ──────────────────────────────────────────────────

    def __repr__(self) -> str:
        """
        ====================================================================
         Multi-line aligned block. Blank line between groups
         when constructed with grouped names.

         Counters(
           cnt_h_search   =   25
           cnt_h_update   =   21

           cnt_phi_search =   13
           cnt_phi_update =   13

           cnt_push       =   16
           cnt_pop        =   13
           cnt_pop_stale  =    3
           cnt_decrease   =    0
         )
        ====================================================================
        """
        if not self._names:
            return 'Counters()'
        w_name = max(len(n) for n in self._names)
        w_val = max(len(str(self._values[n]))
                    for n in self._names)
        lines: list[str] = ['Counters(']
        for gi, group in enumerate(self._groups):
            if gi > 0:
                lines.append('')
            for n in group:
                v = self._values[n]
                lines.append(
                    f'  {n:<{w_name}} = {v:>{w_val}}')
        lines.append(')')
        return '\n'.join(lines)
