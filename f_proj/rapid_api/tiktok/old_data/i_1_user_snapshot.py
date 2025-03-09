from f_proj.rapid_api.tiktok.data.i_0_abc import DataABC, dataclass, field


@dataclass
class DataUserSnapshot(DataABC):
    """
    ============================================================================
     DataClass for User-Snapshot.
    ============================================================================
    """
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
