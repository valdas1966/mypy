from dataclasses import dataclass
from datetime import datetime


@dataclass
class ResponseGemini:
    """
    ========================================================================
     Response from Gemini API — text content and metadata.
    ========================================================================
    """

    text: str
    model: str
    input_tokens: int
    output_tokens: int
    finish_reason: str
    started: datetime
    elapsed: float

    def __repr__(self) -> str:
        """
        ====================================================================
         Return a debug representation.
        ====================================================================
        """
        ts = self.started.strftime('%Y-%m-%d %H:%M:%S')
        return (f'ResponseGemini(model={self.model}, '
                f'in={self.input_tokens}, '
                f'out={self.output_tokens}, '
                f'finish={self.finish_reason}, '
                f'started={ts}, '
                f'elapsed={self.elapsed:.2f}s)')
