from pydantic import Field
from f_proj.rapid_api.data.i_0_user_info import DataUserInfo
from f_proj.rapid_api.data.i_0_user_stats import DataUserStats


class DataUser(DataUserInfo, DataUserStats):
    """
    ============================================================================
     Data-Class for User's Data.
    ============================================================================
    """
    info: DataUserInfo = Field(default=None, alias='user')
    stats: DataUserStats = Field(default=None, alias='stats')
    
    
