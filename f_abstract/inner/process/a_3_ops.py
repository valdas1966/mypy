from f_abstract.inner.process.a_2_globs import ProcessGlobs


class ProcessOps(ProcessGlobs):
    """
    ============================================================================
     Description: List of Operations and List of their Arguments (dicts).
    ============================================================================
    """

    # list[Operation] : List of Operations to Execute
    _ops = None

    # list[dict] : List of Operations-Arguments
    _arg_ops = None
