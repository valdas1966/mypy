from f_core.inner.operation.a_3_log import OperationLog


class Operation(OperationLog):
    """
    ============================================================================
     Inheritance:
    ----------------------------------------------------------------------------
        1. Inittable (init kwargs).
        2. Runnable (pre_run, run, post_run, on_error).
        3. Tittable (title).
        4. Validdable (is_valid, e_msg).
        5. Loggable (pre_log, post_log, log).
    ----------------------------------------------------------------------------
     Inner:
    ----------------------------------------------------------------------------
        1. Init (Init all the Inheritances).
        2. DT (Start & Finish DateTimes).
        3. Log (Pre & Post Logging).
    ============================================================================
    """
    pass
