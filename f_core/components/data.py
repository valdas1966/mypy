from dataclasses import dataclass, field, asdict
from f_core.abstracts.dictable import Dictable


@dataclass
class Data(Dictable):
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
