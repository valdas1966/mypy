from pydantic import Field
from typing import ClassVar
from f_proj.rapid_api.data.i_0_audit import DataAudit
from f_proj.rapid_api.data.i_1_video import DataVideo
from f_proj.rapid_api.data.i_1_music import DataMusic


class DataVideo(DataAudit):
    """
    ============================================================================
     Data-Class for Video.
    ============================================================================
    """
    video: DataVideo = Field(default=None, alias='video_info')
    music: DataMusic = Field(default=None, alias='music_info')
