from f_core.abstracts.dictable import Dictable
from dataclasses import dataclass, asdict


@dataclass
class DataUserSnapshot(Dictable):
    """
    ============================================================================
     DataClass for User-Snapshot.
    ============================================================================
    """
    is_ok = bool
    is_found = bool
    source = str
    id_user = str
    nick = str
    is_verified = bool
    is_secret = bool
    is_private = bool
    following = int
    followers = int
    videos = int
    hearts = int
    diggs = int

    def to_dict(self) -> dict:
        """
        ========================================================================
         Convert the DataClass into a Dict.
        ========================================================================
        """
        return asdict(self)
