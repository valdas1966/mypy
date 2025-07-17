from dataclasses import dataclass, asdict
from f_core.mixins.dictable.main import Dictable


@dataclass(frozen=True)
class DataFrozen(Dictable):
    """
    ============================================================================
     Base Data-Class.
    ============================================================================
    """

    def to_dict(self) -> dict[str, any]:
        """
        ========================================================================
         Convert the DataClass into a Dict.
        ========================================================================
        """
        return asdict(self)
