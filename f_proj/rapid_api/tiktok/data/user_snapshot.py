from f_core.components.data import Data, dataclass, field


@dataclass
class DataUserSnapshot(Data):
    """
    ============================================================================
     DataClass for User-Snapshot.
    ============================================================================
    """
    is_ok: bool = field(default=None)
    is_found: bool = field(default=None)
    source: str = field(default=None)
    id_user: str = field(default=None)
    nick: str = field(default=None)
    is_verified: bool = field(default=None)
    is_secret: bool = field(default=None)
    is_private: bool = field(default=None)
    following: int = field(default=None)
    followers: int = field(default=None)
    videos: int = field(default=None)
    hearts: int = field(default=None)
    diggs: int = field(default=None)
