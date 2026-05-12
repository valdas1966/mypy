from f_core.recorder import Recorder


class _OnGoalToOnStartShim:
    """
    ========================================================================
     Recorder shim that intercepts events on the way to a real
     `Recorder`, rewriting `on_goal` events into `on_start`
     events (and `goal_index` payload field into `start_index`).

     Used by `KBFSMOSPP` and `KDijkstraMOSPP` to delegate to
     the OMSPP `KBFS` / `KDijkstra` orchestrators (which emit
     `on_goal` events natively) while keeping the MOSPP
     recording convention (`on_start`, `start_index`). Push /
     pop / decrease_g events pass through unchanged.

     Exposes the minimal `Recorder` surface that `AlgoSPP` /
     `AlgoOMSPP` touch: the `is_active` property and the
     `record(event)` method. The shim's `is_active` mirrors
     the wrapped target — set MOSPP's recorder state and the
     inner OMSPP follows.

     This is intentionally a narrow, MOSPP-local utility — not
     in `f_core`. Two callers today (`KBFSMOSPP`,
     `KDijkstraMOSPP`); extract if MMSPP later grows a third.
    ========================================================================
    """

    def __init__(self, target: Recorder) -> None:
        """
        ====================================================================
         Init private Attributes. `target` is the real recorder
         that receives the (possibly-rewritten) events.
        ====================================================================
        """
        self._target: Recorder = target

    @property
    def is_active(self) -> bool:
        """
        ====================================================================
         Delegated to the wrapped target.
        ====================================================================
        """
        return self._target.is_active

    def record(self, event: dict) -> None:
        """
        ====================================================================
         Rewrite `on_goal` → `on_start` (and `goal_index` →
         `start_index`) before forwarding; pass everything else
         through unchanged.
        ====================================================================
        """
        if event.get('type') == 'on_goal':
            event = dict(event)
            event['type'] = 'on_start'
            if 'goal_index' in event:
                event['start_index'] = event.pop('goal_index')
        self._target.record(event)
