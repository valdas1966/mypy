from pydantic import Field
from f_psl.pydantic.mixins.flattenable import Flattenable


class DataUserStats(Flattenable):
    """
    ============================================================================
     Data-Class for User's Stats.
    ============================================================================
    """
    videos: int = Field(default=None, alias='videoCount')
    hearts: int = Field(default=None, alias='heartCount')
    diggs: int = Field(default=None, alias='diggCount')
    followers: int = Field(default=None, alias='followerCount')
    following: int = Field(default=None, alias='followingCount')
    