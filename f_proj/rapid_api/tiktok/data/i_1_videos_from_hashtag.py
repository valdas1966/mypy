from f_proj.rapid_api.tiktok.data.i_0_abc import DataABC, dataclass, field


@dataclass
class DataVideosFromHashtag(DataABC):
    """
    ============================================================================
     DataClass for Videos from Hashtag.
    ============================================================================
    """
    id_hashtag: str = field(default=None)
    id_user: str = field(default=None)
    id_user_unique: str = field(default=None)
    nick: str = field(default=None)
    region: str = field(default=None)
    id_video: str = field(default=None)
    title: str = field(default=None)
    created: int = field(default=None)
    duration: int = field(default=None)
    plays: int = field(default=None)
    shares: int = field(default=None)
    diggs: int = field(default=None)
    downloads: int = field(default=None)
    comments: int = field(default=None)
    is_ad: bool = field(default=None)
