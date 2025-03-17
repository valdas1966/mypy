from pydantic import Field
from f_proj.rapid_api.data.i_0_audit import DataAudit


class DataVideo(DataAudit):
    """
    ============================================================================
     Data-Class for Video.
    ============================================================================
    """
    id_video: str = Field(default=None, alias='video_id')
    created: int = Field(default=None, alias='create_time')
    region: str = Field(default=None, alias='region')
    title: str = Field(default=None, alias='title')
    duration: int = Field(default=None, alias='duration')
    plays: int = Field(default=None, alias='play_count')
    shares: int = Field(default=None, alias='share_count')
    diggs: int = Field(default=None, alias='digg_count')
    comments: int = Field(default=None, alias='comment_count')
    downloads: int = Field(default=None, alias='download_count')
    is_ad: bool = Field(default=None, alias='is_ad')
    play: int = Field(default=None, alias='play')
    