from f_proj.rapid_api.tiktok.data.i_0_abc import DataABC, dataclass, field


@dataclass
class DataCommentsFromVideos(DataABC):
    """
    ============================================================================
     DataClass for Comments from Videos.
    ============================================================================
    """
    id_comment: str = field(default=None)
    text: str = field(default=None)
    id_video: str = field(default=None)
    diggs: int = field(default=None)
    replies: int = field(default=None)
    created: int = field(default=None)
    id_user: str = field(default=None)
    id_user_unique: str = field(default=None)
    nick: str = field(default=None)
    region: str = field(default=None)
    aweme: int = field(default=None)
    favorited: int = field(default=None)
    followers: int = field(default=None)
    following: int = field(default=None)
    
