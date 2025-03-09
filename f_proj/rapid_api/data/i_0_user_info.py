from pydantic import BaseModel, Field


class DataUserInfo(BaseModel):
    """
    ============================================================================
     Data-Class for User's Info.
    ============================================================================
    """
    id_user: str = Field(default=None, alias='user_id')
    id_user_unique: str = Field(default=None, alias='user_unique_id')
    nick: str = Field(default=None, alias='nickname')
    is_verified: bool = Field(default=None, alias='is_verified')
    is_secret: bool = Field(default=None, alias='is_secret')
    is_private: bool = Field(default=None, alias='is_private')   
    
