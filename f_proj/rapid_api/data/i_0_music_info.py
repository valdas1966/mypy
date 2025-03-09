from pydantic import Field
from f_psl.pydantic.mixins.flattenable import Flattenable


class DataMusicInfo(Flattenable):
    """
    ============================================================================
     Data-Class for Music's Info.
    ============================================================================
    """
    id_music: str = Field(default=None, alias='id')
