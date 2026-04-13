from dataclasses import dataclass
from datetime import datetime


@dataclass
class ResponseGemini:
    """
    ========================================================================
     Response from Gemini API — text content and metadata.
    ========================================================================
    """

    # (input_per_M, output_per_M) in dollars
    _COST_PER_M = {
        'gemini-2.5-flash': (0.15, 0.60),
        'gemini-2.5-pro':   (1.25, 10.00),
        'gemini-2.0-flash': (0.10, 0.40),
    }

    text: str
    model: str
    input_tokens: int
    output_tokens: int
    finish_reason: str
    started: datetime
    elapsed: float

    @property
    def cost(self) -> float | None:
        """
        ====================================================================
         Cost of this API call in dollars. None if model pricing unknown.
        ====================================================================
        """
        if not self._COST_PER_M:
            return None
        prices = self._COST_PER_M.get(self.model)
        if not prices:
            return None
        inp, out = prices
        return ((self.input_tokens * inp
                 + self.output_tokens * out) / 1_000_000)

    def __repr__(self) -> str:
        """
        ====================================================================
         Return a debug representation.
        ====================================================================
        """
        ts = self.started.strftime('%Y-%m-%d %H:%M:%S')
        cost = self.cost
        cost_str = f', cost=${cost:.6f}' if cost is not None else ''
        # Truncate text to 50 chars for readability
        text = self.text
        if len(text) > 50:
            text = text[:47] + '...'
        return (f'ResponseGemini(text={text}, '
                f'model={self.model}, '
                f'in={self.input_tokens}, '
                f'out={self.output_tokens}, '
                f'finish={self.finish_reason}, '
                f'started={ts}, '
                f'elapsed={self.elapsed:.2f}s'
                f'{cost_str})')
