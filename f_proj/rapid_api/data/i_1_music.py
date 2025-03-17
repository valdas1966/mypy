from pydantic import Field
from f_psl.pydantic.mixins.flattenable import Flattenable


class DataMusic(Flattenable):
    """
    ============================================================================
     Data-Class for Music.
    ============================================================================
    """ 
    id_music: str = Field(default=None, alias='id')
    