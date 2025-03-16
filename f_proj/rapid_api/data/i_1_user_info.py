from pydantic import Field
from f_psl.pydantic.mixins.flattenable import Flattenable


class DataUserInfo(Flattenable):
    """
    ============================================================================
     Data-Class for User's Info.
    ============================================================================
    """
    id_user: str = Field(default=None, alias='id')
    id_user_unique: str = Field(default=None, alias='uniqueId')
    nick: str = Field(default=None, alias='nickname')
    is_verified: bool = Field(default=None, alias='verified')
    is_secret: bool = Field(default=None, alias='secret')
    is_private: bool = Field(default=None, alias='private')   
