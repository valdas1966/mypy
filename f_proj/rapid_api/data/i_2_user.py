from pydantic import Field
from f_proj.rapid_api.data.i_0_audit import DataAudit
from f_proj.rapid_api.data.i_1_user_info import DataUserInfo
from f_proj.rapid_api.data.i_1_user_stats import DataUserStats


class DataUser(DataAudit):
    """
    ============================================================================
     Data-Class for User's Data.
    ============================================================================
    """
    info: DataUserInfo = Field(default=None, alias='user')
    stats: DataUserStats = Field(default=None, alias='stats')
    
    
