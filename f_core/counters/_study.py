"""
================================================================================
 Study: Counters.absorb() — mirroring counters across components.
================================================================================
 `absorb` copies counters from a source Mapping into this
 Counters by absolute assignment, synthesizing a `default` for
 any name the source does not track. The motivating use case
 is an algorithm mirroring a frontier's heap-op tally at
 end-of-run — where a FIFO frontier has no `cnt_decrease`.

 Run:  python -m f_core.counters._study
================================================================================
"""

from f_core.counters import Counters


def study_mirror_priority_frontier() -> None:
    """
    ============================================================================
     Priority frontier → algo: all three heap-op names are
     present in the source, so all three mirror across.
    ============================================================================
    """
    # A priority frontier owns push/pop/decrease; it has run.
    frontier = Counters.Factory.frontier_priority()
    frontier.inc('cnt_push', n=16)
    frontier.inc('cnt_pop', n=13)
    frontier.inc('cnt_decrease', n=4)
    # The algo has a wider scaffold; mirror the heap-op block.
    algo = Counters.Factory.algo()
    algo.absorb(frontier,
                names=('cnt_push', 'cnt_pop', 'cnt_decrease'))
    print('1) priority frontier → algo (all present):')
    print(algo)


def study_mirror_fifo_frontier() -> None:
    """
    ============================================================================
     FIFO frontier → algo: the source has no `cnt_decrease`,
     so `absorb` writes the structural default 0 — no
     `'cnt_decrease' in fc` guard at the call site.
    ============================================================================
    """
    # A FIFO frontier owns only push/pop (no decrease op).
    frontier = Counters.Factory.frontier_fifo()
    frontier.inc('cnt_push', n=9)
    frontier.inc('cnt_pop', n=9)
    # Mirror the SAME three names; cnt_decrease is absent in
    # the source, so absorb synthesizes the structural 0.
    algo = Counters.Factory.algo()
    algo.absorb(frontier,
                names=('cnt_push', 'cnt_pop', 'cnt_decrease'))
    print('2) fifo frontier → algo (decrease synthesized 0):')
    print(algo)


def study_full_schema_default() -> None:
    """
    ============================================================================
     With `names=None`, `absorb` walks this Counters' full
     schema. Names absent from the source take `default` —
     shown here with a non-zero default to make the fill
     visible.
    ============================================================================
    """
    source = Counters(names=('cnt_push', 'cnt_pop'))
    source.inc('cnt_push', n=3)
    target = Counters(names=(
        'cnt_push', 'cnt_pop', 'cnt_decrease'))
    target.absorb(source, default=-1)
    print('3) names=None, default=-1 fills missing decrease:')
    print(target.as_dict())


if __name__ == '__main__':
    study_mirror_priority_frontier()
    print()
    study_mirror_fifo_frontier()
    print()
    study_full_schema_default()
