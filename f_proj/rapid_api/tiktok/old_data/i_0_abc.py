from f_core.components.data import Data, dataclass, field


@dataclass
class DataABC(Data):
    """
    ============================================================================
     ABC Data-Class for TikTok requests.
    ============================================================================
    """
    is_ok: bool = field(default=None)
    is_found: bool = field(default=None)
    is_broken: bool = field(default=None)
    status_code: int = field(default=None)
    msg: str = field(default=None)
