from f_proj.rapid_api.data.i_0_list import DataList
from f_proj.rapid_api.data.i_1_video import DataVideo
from typing import ClassVar


class DataVideosByUser(DataList[DataVideo]):
    """
    ============================================================================
     Data-Class for Videos by User.
    ============================================================================
    """
    rows_key: ClassVar[str] = 'videos'

    class Config:
        """
        ============================================================================
         Config for request 'Videos by User'.
        ============================================================================
        """
        populate_by_name = True
        extra = 'allow'  # allows setting arbitrary attributes like 'is_ok'
