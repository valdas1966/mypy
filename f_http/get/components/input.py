from dataclasses import dataclass, field


@dataclass
class InputRequest:
    """
    ============================================================================
     InputRequest of Http Get-Request.
    ============================================================================
    """
    url: str
    params: dict[str, str] = field(default_factory=dict)
    headers: dict[str, str] = field(default_factory=dict)
