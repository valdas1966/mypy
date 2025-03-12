from pydantic import Field
from f_proj.rapid_api.data.i_0_audit import DataAudit


class DataHashtag(DataAudit):
    """
    ============================================================================
     Data-Class for Hashtag.
    ============================================================================
    """
    id_hashtag: str = Field(default=None, alias='id')
    name: str = Field(default=None, alias='cha_name')
    users: int = Field(default=None, alias='user_count')
    views: int = Field(default=None, alias='view_count')
    