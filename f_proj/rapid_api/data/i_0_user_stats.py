from pydantic import BaseModel, Field


class DataUserStats(BaseModel):
    """
    ============================================================================
     Data-Class for User's Stats.
    ============================================================================
    """
    videos: int = Field(default=None, alias='video_count')
    hearts: int = Field(default=None, alias='heart_count')
    diggs: int = Field(default=None, alias='digg_count')
    followers: int = Field(default=None, alias='follower_count')
    following: int = Field(default=None, alias='following_count')
    
    
    
