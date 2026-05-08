import sys

from f_core.counters.main import Counters
from f_cs.algo import Algo
from f_hs.algo.i_0_oospp.i_0_base._search_state import SearchStateSPP
from f_hs.frontier.i_0_base.main import FrontierBase
from f_hs.problem.i_0_base.main import ProblemSPP
from f_hs.solution.main import SolutionSPP
from f_hs.state.i_0_base.main import StateBase
from time import perf_counter_ns
from typing import Any, Generic, TypeVar

State = TypeVar('State', bound=StateBase)


class AlgoSPP(Generic[State], Algo[ProblemSPP[State], SolutionSPP]):
    """
    ============================================================================
     Base Algorithm for Shortest-Path-Problem.
    ============================================================================
    """

    def __init__(self,
                 problem: ProblemSPP[State],
                 frontier: FrontierBase[State],
                 name: str = 'AlgoSPP',
                 is_recording: bool = False,
                 search_state: SearchStateSPP[State] | None = None
                 ) -> None:
        """
        ====================================================================
         Init private Attributes.

         `search_state` — optional pre-built SearchStateSPP to
         inject (e.g., seed a mid-search state for a test, or
         feed an iterative OMSPP sub-search with warm g/parent
         dicts). When supplied, the `frontier` argument is
         ignored (the caller's `search_state.frontier` wins).
         Consumers who inject should call `resume()` rather
         than `run()`, since `run() → _init_search` clears the
         bundle before pumping.
        ====================================================================
        """
        Algo.__init__(self, problem=problem, name=name,
                      is_recording=is_recording)
        # Per-search dynamic state (frontier + g + parent + closed +
        # goal_reached + cache_hit). Mutated during the loop, exposed
        # via `search_state` for cross-instance peeking and for
        # caller-driven seeding.
        self._search: SearchStateSPP[State] = (
            search_state if search_state is not None
            else SearchStateSPP(frontier=frontier))
        # Cached lookup set, derived from the (immutable) problem.
        # Populated at init (not only in _init_search) so a
        # caller who uses `resume()` straight after construction
        # still has a working goal check.
        self._goals_set: set[State] = set(self.problem.goals)
        # Dirty flag — when a caller injects a SearchStateSPP
        # whose frontier entries were pushed with priorities
        # computed against a stale heuristic or goal, the next
        # resume() refreshes them. Cleared after refresh; also
        # cleared by `_init_search` (which rebuilds the frontier
        # from scratch, making any stale priorities irrelevant).
        self._frontier_dirty: bool = search_state is not None
        # Seed the event-duration clock so pre-search events
        # (e.g., `propagate` emitted from pathmax before
        # `_run_pre` fires) can compute a valid `duration`.
        # `_run_pre` will reset this later for search timing.
        self._event_prev_ns: int = perf_counter_ns()
        # Own-scaffold Counters:
        # - heap-op group (cnt_push / cnt_pop / cnt_decrease) is
        #   mirrored from the injected frontier on every
        #   `counters` access (frontier is single source of
        #   truth);
        # - search-semantic group (cnt_expanded / cnt_generated)
        #   is incremented inline by `_search_loop`,
        #   `_handle_child`, and `_init_search` (start seed);
        # - memory group (mem_open / mem_closed) is snapshotted
        #   in `_run_post()` AFTER the timer closes (outside the
        #   runtime budget).
        # `mem_open` includes per-state g/parent share for states
        # currently in OPEN; `mem_closed` includes the same share
        # for states NOT in OPEN (closed + popped-but-not-closed
        # goal). The two split exactly the search-state
        # bookkeeping memory by membership.
        self._counters: Counters = Counters(names=(
            ('cnt_push', 'cnt_pop', 'cnt_decrease'),
            ('cnt_expanded', 'cnt_generated'),
            ('mem_open', 'mem_closed'),
        ))
        self._mem: dict[str, int] = {}

    # ──────────────────────────────────────────────────
    #  Public Properties
    # ──────────────────────────────────────────────────

    @property
    def search_state(self) -> SearchStateSPP[State]:
        """
        ====================================================================
         The dynamic per-search state. Read-access for consumers
         that need to inspect frontier/closed/g across instances
         (e.g. bidirectional search), and the resumability anchor.
        ====================================================================
        """
        return self._search

    @property
    def counters(self) -> Counters:
        """
        ====================================================================
         6-name scaffold (3 op-counters + 3 mem-snapshots).

         Heap-op counters are mirrored from the injected
         frontier on every access (`cnt_push`, `cnt_pop`,
         `cnt_decrease`). Memory snapshots (`mem_open`,
         `mem_closed`, `mem_g_parent`) are populated in
         `_run_post()` AFTER the timer closes — they are NOT
         in the runtime budget.

         Subclasses can extend the snapshot via the
         `_memory_snapshot()` hook (`super()._memory_snapshot()`
         + add fields).
        ====================================================================
        """
        fc = self._search.frontier.counters
        self._counters.assign('cnt_push', fc['cnt_push'])
        self._counters.assign('cnt_pop', fc['cnt_pop'])
        self._counters.assign('cnt_decrease', fc['cnt_decrease'])
        for k, v in self._mem.items():
            self._counters.assign(k, v)
        return self._counters

    # ──────────────────────────────────────────────────
    #  Memory Snapshot (subclass hook)
    # ──────────────────────────────────────────────────

    def _memory_snapshot(self) -> dict[str, int]:
        """
        ====================================================================
         Return per-class memory snapshot (bytes) at the
         current `self._search` state. Called from
         `_run_post()` AFTER the elapsed timer has been
         recorded by the inherited `_run_post`, so the cost of
         this measurement is structurally OUT of `_elapsed`.

         Subclasses that hold additional persistent state
         (HCached / HBounded dicts, etc.) extend this via
         `snap = super()._memory_snapshot(); snap[...] = ...`
         and then return the augmented dict.

         Universal fields (every OOSPP algo):
           - `mem_open`   : frontier internal structures
                            (FrontierPriority: heap + index +
                            tuples; FrontierFIFO: deque) +
                            g/parent slot share for states
                            CURRENTLY in OPEN.
           - `mem_closed` : closed-set bucket array + g/parent
                            slot share for states NOT in OPEN
                            (closed states + the
                            popped-but-not-closed goal).

         g/parent dicts hold one slot per discovered state.
         `sys.getsizeof()` reports the dict-wide size; we
         pro-rate it by membership: per-entry = total / |g|,
         then multiply by |open| (charged to mem_open) and
         |g|-|open| (charged to mem_closed). This matches
         CPython's uniform per-entry slot cost within a single
         dict — the pro-rate is exact for slot accounting.

         All numbers come from `sys.getsizeof()` — CPython's
         own accounting. Shared State objects are NOT
         double-counted (parent dict's State values are shared
         with closed/frontier and not summed).
        ====================================================================
        """
        fr = self._search.frontier
        queue = getattr(fr, '_queue', None)
        if queue is not None and hasattr(queue, '_heap'):
            frontier_struct = (sys.getsizeof(queue._heap)
                               + sys.getsizeof(queue._index)
                               + sum(sys.getsizeof(t)
                                     for t in queue._heap))
        else:
            frontier_struct = sys.getsizeof(
                queue if queue is not None else fr)
        closed = self._search.closed
        g = self._search.g
        parent = self._search.parent
        n_g = len(g)
        n_open = len(fr)
        if n_g > 0:
            g_parent_total = (sys.getsizeof(g)
                              + sum(sys.getsizeof(v)
                                    for v in g.values())
                              + sys.getsizeof(parent))
            per_entry = g_parent_total / n_g
            g_parent_open = round(per_entry * n_open)
            g_parent_closed = round(per_entry * (n_g - n_open))
        else:
            g_parent_open = 0
            g_parent_closed = 0
        return {
            'mem_open':   frontier_struct + g_parent_open,
            'mem_closed': sys.getsizeof(closed) + g_parent_closed,
        }

    def _run_post(self) -> None:
        """
        ====================================================================
         Records `_elapsed` via super, THEN takes the memory
         snapshot. The snapshot lives outside the runtime
         budget by construction — `super()._run_post()`
         captures `_elapsed` before this method's snapshot
         work runs.
        ====================================================================
        """
        super()._run_post()
        self._mem = self._memory_snapshot()

    # ──────────────────────────────────────────────────
    #  Lifecycle
    # ──────────────────────────────────────────────────

    def _run(self) -> SolutionSPP:
        """
        ====================================================================
         Initialize the search and run the loop. Public entry via
         the inherited run().
        ====================================================================
        """
        self._init_search()
        return self._search_loop()

    def resume(self) -> SolutionSPP:
        """
        ====================================================================
         Continue the search from current state without
         re-initializing. Reuses ProcessBase's lifecycle plumbing
         (timing reset + output capture) but skips _init_search,
         so frontier / closed / g / parent / recorder are
         preserved.

         If the frontier is marked dirty (caller injected a
         SearchStateSPP at __init__), refresh priorities before
         pumping — re-computing `_priority(state)` for every
         state on the frontier. Refresh is O(n log n) on the
         frontier size; subsequent resume() calls see a clean
         frontier and skip the refresh.

         Used by OMSPP-iterative pumping, bidirectional search,
         and caller-seeded recording tests.
        ====================================================================
        """
        if self._frontier_dirty:
            self.refresh_priorities()
        self._run_pre()
        self._output = self._search_loop()
        self._run_post()
        return self._output

    def refresh_priorities(self) -> None:
        """
        ====================================================================
         Recompute the priority of every State currently on the
         frontier and rebuild the frontier with the fresh values.
         Safe with non-monotone changes (priorities may go up
         OR down) — uses drain-and-push rather than `decrease`,
         since FrontierPriority's `decrease` rejects higher
         priorities.

         Does NOT emit recorder events (the refresh is setup,
         not a search step). Clears the dirty flag on success.
        ====================================================================
        """
        states: list[State] = list(self._search.frontier)
        self._search.frontier.clear()
        for s in states:
            self._search.frontier.push(
                state=s,
                priority=self._priority(state=s),
            )
        self._frontier_dirty = False

    # ──────────────────────────────────────────────────
    #  Search Initialization
    # ──────────────────────────────────────────────────

    def _init_search(self) -> None:
        """
        ====================================================================
         Initialize the Search.

         **Recorder is NOT cleared here** (as of Phase 2b's
         pre-search `propagate` events). Events recorded before
         `run()` — e.g., from `propagate_pathmax` — must persist
         into the search log so consumers see the full timeline.
         Callers who want a fresh log across `run()` invocations
         should call `self.recorder.clear()` explicitly.

         Counters ARE reset here (run-only; resume() preserves
         them — needed for OMSPP-iterative accumulation).
        ====================================================================
        """
        self._search.clear()
        self._counters.reset()
        self._goals_set = set(self.problem.goals)
        for start in self.problem.starts:
            self._search.g[start] = 0.0
            self._search.parent[start] = None
            self._counters.inc('cnt_generated')
            self._push(state=start)
        # Frontier is freshly rebuilt with current priorities —
        # any stale-priority concerns from an injected seed are
        # moot after a full init.
        self._frontier_dirty = False

    # ──────────────────────────────────────────────────
    #  Search Loop (Classical Pseudocode)
    # ──────────────────────────────────────────────────

    def _search_loop(self) -> SolutionSPP:
        """
        ====================================================================
         Pump the search loop until a Goal is popped or the
         Frontier is exhausted. Does NOT initialize — callable
         after _init_search (via _run) or directly (via resume).

         `_early_exit` runs after pop and before the goal check;
         it short-circuits the loop when a subclass (AStarLookup
         with HCached) can terminate via perfect-h on the popped
         state.

         `_pre_expand` runs after close and before the successor
         loop; it's the hook where AStarBPMX applies BPMX
         (in-search pathmax) to lift h values of the current
         state and its neighbours before they get priorities.
        ====================================================================
        """
        while self._search.frontier:
            state = self._pop()
            sol = self._early_exit(state=state)
            if sol is not None:
                return sol
            if self._is_goal(state):
                self._search.goal_reached = state
                return SolutionSPP(cost=self._search.g[state])
            self._close(state)
            self._counters.inc('cnt_expanded')
            self._pre_expand(state=state)
            for child in self.problem.successors(state):
                self._handle_child(parent=state,
                                   child=child)
        return SolutionSPP(cost=float('inf'))

    # ──────────────────────────────────────────────────
    #  Early-Exit Hook (subclass override)
    # ──────────────────────────────────────────────────

    def _early_exit(self, state: State) -> SolutionSPP | None:
        """
        ====================================================================
         Subclass hook — return a SolutionSPP to short-circuit
         the loop immediately after popping `state`, or None to
         continue with the normal goal-check + expansion. Default:
         never short-circuit. AStarLookup overrides to terminate
         on an HCached perfect-h hit.
        ====================================================================
        """
        return None

    def _pre_expand(self, state: State) -> None:
        """
        ====================================================================
         Subclass hook — runs after close and before the
         successor loop at each expansion. Default: no-op.
         AStarBPMX overrides (via BPMXMixin) for in-search
         pathmax: Rules 1, 2, 3, CASCADE.
        ====================================================================
        """
        pass

    # ──────────────────────────────────────────────────
    #  Core Operations
    # ──────────────────────────────────────────────────

    def _is_goal(self, state: State) -> bool:
        """
        ====================================================================
         Return True if the State is a Goal.
        ====================================================================
        """
        return state in self._goals_set

    def _close(self, state: State) -> None:
        """
        ====================================================================
         Close the State (mark as expanded).
        ====================================================================
        """
        self._search.closed.add(state)

    def _handle_child(self,
                      parent: State,
                      child: State) -> None:
        """
        ====================================================================
         Handle a Child State discovered from Parent.
        ====================================================================
        """
        if child in self._search.closed:
            return
        new_g = (self._search.g[parent]
                 + self.problem.w(parent=parent,
                                  child=child))
        if child not in self._search.frontier:
            self._search.g[child] = new_g
            self._search.parent[child] = parent
            self._counters.inc('cnt_generated')
            self._push(state=child)
        elif new_g < self._search.g[child]:
            self._search.g[child] = new_g
            self._search.parent[child] = parent
            self._decrease_g(state=child)

    # ──────────────────────────────────────────────────
    #  Frontier Wrappers (with recording)
    # ──────────────────────────────────────────────────

    def _push(self, state: State) -> None:
        """
        ====================================================================
         Push a State into the Frontier and record.
        ====================================================================
        """
        self._search.frontier.push(
            state=state,
            priority=self._priority(state=state),
        )
        self._record_event(type='push', state=state)

    def _pop(self) -> State:
        """
        ====================================================================
         Pop the next State from the Frontier and record.
        ====================================================================
        """
        state = self._search.frontier.pop()
        self._record_event(type='pop', state=state)
        return state

    def _decrease_g(self, state: State) -> None:
        """
        ====================================================================
         Update Priority in the Frontier and record.
        ====================================================================
        """
        self._search.frontier.decrease(
            state=state,
            priority=self._priority(state=state),
        )
        self._record_event(type='decrease_g', state=state)

    # ──────────────────────────────────────────────────
    #  Priority (subclass override)
    # ──────────────────────────────────────────────────

    def _priority(self, state: State) -> Any:
        """
        ====================================================================
         Return the Priority for a State. Default: None (FIFO).
         Subclasses (e.g. AStar) override to compute a priority
         tuple, e.g. (f, -g, state).
        ====================================================================
        """
        return None

    # ──────────────────────────────────────────────────
    #  Event Recording
    # ──────────────────────────────────────────────────

    def _record_event(self,
                      type: str,
                      state: State | None = None,
                      **extra) -> None:
        """
        ====================================================================
         Record a Search Event.

         Auto-fill policy:
           - `g` (as int): added for push / pop / decrease_g.
             Skipped for other types (propagate, propagate_wave,
             and future pre-/post-search events) — they may fire
             with a state not yet in `self._search.g`, or no
             state at all.
           - `parent`: added for push / decrease_g. Skipped for
             pop (the Recording Principle's `parent not in event`
             ⇒ "parenthood isn't applicable here"). Skipped for
             non-search types — callers pass their own via
             **extra when semantically meaningful.

         `state` is optional: meta-events (e.g., `propagate_wave`
         marking the start of a pathmax wave) are not tied to a
         particular state. When `state` is None, the event dict
         omits the key entirely (absent ≠ None convention).

         `**extra` is merged onto the event dict, so callers can
         add arbitrary fields (h_parent for propagate, depth for
         propagate_wave, etc.). Edge cost w is NOT recorded —
         it's derivable.
        ====================================================================
        """
        if not self._recorder:
            return
        event = dict(type=type)
        if state is not None:
            event['state'] = state
        if type in ('push', 'pop', 'decrease_g'):
            event['g'] = int(self._search.g[state])
        if type in ('push', 'decrease_g'):
            event['parent'] = self._search.parent[state]
        event.update(extra)
        super()._record_event(**event)

    # ──────────────────────────────────────────────────
    #  Path Reconstruction
    # ──────────────────────────────────────────────────

    def reconstruct_path(self,
                         goal: State | None = None
                         ) -> list[State]:
        """
        ====================================================================
         Reconstruct the Path from Start to Goal.
        ====================================================================
        """
        target = (goal if goal is not None
                  else self._search.goal_reached)
        if target is None:
            return list()
        path: list[State] = list()
        current: State | None = target
        while current is not None:
            path.append(current)
            current = self._search.parent.get(current)
        path.reverse()
        return path
