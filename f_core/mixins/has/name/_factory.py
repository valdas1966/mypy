from f_core.mixins.has.name.main import HasName


def create_has_name(name: str = None) -> HasName:
    """
    ============================================================================
     Factory function to create HasName instances.
    ============================================================================
    """
    return HasName(name)