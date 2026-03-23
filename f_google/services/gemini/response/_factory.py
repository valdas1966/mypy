from datetime import datetime
from f_google.services.gemini.response.main import ResponseGemini


class Factory:
    """
    ========================================================================
     Factory for ResponseGemini test instances.
    ========================================================================
    """

    @staticmethod
    def gen(text: str = 'Sample response.',
            model: str = 'gemini-2.5-flash',
            input_tokens: int = 10,
            output_tokens: int = 20,
            finish_reason: str = 'STOP',
            started: datetime = None,
            elapsed: float = 1.0) -> ResponseGemini:
        """
        ====================================================================
         Generate a ResponseGemini test instance.
        ====================================================================
        """
        if started is None:
            started = datetime.now()
        return ResponseGemini(text=text,
                              model=model,
                              input_tokens=input_tokens,
                              output_tokens=output_tokens,
                              finish_reason=finish_reason,
                              started=started,
                              elapsed=elapsed)
