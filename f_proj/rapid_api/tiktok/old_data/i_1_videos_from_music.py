from f_proj.rapid_api.tiktok.data.i_0_abc import DataABC, dataclass, field


@dataclass
class DataVideosFromMusic(DataABC):
    """
    ============================================================================
     DataClass for User-Snapshot.
    ============================================================================
    """
    id_music: str = field(default=None)
    id_user: str = field(default=None)
    id_video: str = field(default=None)
