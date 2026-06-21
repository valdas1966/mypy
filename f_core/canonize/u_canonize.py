"""
============================================================================
 Canonical identity projection for keyed framework objects.

 `canonize(v)` renders any value as a clean, comparable PRIMITIVE
 (tuple / int / str / ...) by recursively descending the f_core
 key family:
   - a `HasKey` / `HasRowCol` object  -> descend into its `.key`,
   - a `tuple` / `list`               -> canonize element-wise,
   - anything else (primitive / None) -> return unchanged.

 This is f_core's own key-projection plumbing. It is defined purely
 over the `HasKey` / `HasRowCol` mixins (it is a *sibling* of them,
 not a method on them), so it lives beside `mixins/`, not inside it.
 Placement follows the dispatch targets: `canonize` must sit at or
 below the lowest layer of the types it descends (the mixins live in
 f_core, and `CellMap` -- a `HasRowCol` -- lives in f_ds, above
 f_core), so f_core is the only home that serves every keyed object
 (f_ds cells, f_hs states, future) without a backward import.

 It exists so that every keyed object renders its identity ONCE,
 here, instead of each subclass re-hand-rolling an unwrap
 (e.g. `StateCell -> (row, col)`, `StateRC -> ((row, col), budget)`).

 Primary consumers: recording-test golden normalizers and
 visualization traces, which compare / print identities as Python
 literals and therefore need a primitive, not a live object.
============================================================================
"""
from f_core.mixins.has.key import HasKey
from f_core.mixins.has.row_col import HasRowCol


def canonize(v: object) -> object:
    """
    ========================================================================
     Return the canonical PRIMITIVE identity of `v`.

     Recursively descends keyed objects (`HasKey` / `HasRowCol`)
     into their `.key`, walks `tuple` / `list` element-wise
     (preserving container type), and passes primitives (`int`,
     `str`, `None`, ...) through unchanged. Idempotent on the
     result: `canonize(canonize(v)) == canonize(v)`.
    ========================================================================
    """
    # Keyed object -> descend into its key
    if isinstance(v, (HasKey, HasRowCol)):
        return canonize(v.key)
    # Container -> canonize element-wise, preserving type
    if isinstance(v, (tuple, list)):
        return type(v)(canonize(x) for x in v)
    # Primitive / None -> unchanged
    return v
