
class MixinIdAutoIncrement:
    """
    ============================================================================
     Desc: Mixin for AutoIncrement-ID Property.
    ============================================================================
     Properties:
    ----------------------------------------------------------------------------
        1. id (int) : Object ID.
    ============================================================================
    """

    # Class-Attribute for AutoIncrementing-ID
    _id_last = 0

    def __init__(self) -> None:
        """
        ========================================================================
         Desc: Increment the Class-Last-ID and Assign to this instance.
        ========================================================================
        """
        MixinIdAutoIncrement._id_last += 1
        self._id = MixinIdAutoIncrement._id_last

    @property
    def id(self) -> int:
        return self._id
