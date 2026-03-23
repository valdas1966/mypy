import time
from datetime import datetime
import vertexai
from google.oauth2.service_account import Credentials as SACredentials
from vertexai.generative_models import GenerativeModel
from f_google.services.gemini.response.main import ResponseGemini


class Gemini:
    """
    ========================================================================
     Google Gemini Service Wrapper (via Vertex AI).
    ========================================================================
    """

    # Factory
    Factory: type = None

    _DEFAULT_MODEL = 'gemini-2.5-flash'

    def __init__(self,
                 creds: SACredentials,
                 model: str = None,
                 location: str = 'us-central1') -> None:
        """
        ====================================================================
         Init Gemini Client with SA Credentials.
        ====================================================================
        """
        self._model_name = model or self._DEFAULT_MODEL
        vertexai.init(project=creds.project_id,
                      location=location,
                      credentials=creds)
        self._model = GenerativeModel(self._model_name)

    def ask(self, prompt: str) -> ResponseGemini:
        """
        ====================================================================
         Send a text prompt and return a ResponseGemini.
        ====================================================================
        """
        started = datetime.now()
        t_start = time.perf_counter()
        response = self._model.generate_content(prompt)
        elapsed = time.perf_counter() - t_start
        usage = response.usage_metadata
        return ResponseGemini(
            text=response.text,
            model=self._model_name,
            input_tokens=usage.prompt_token_count,
            output_tokens=usage.candidates_token_count,
            finish_reason=response.candidates[0]
                          .finish_reason.name,
            started=started,
            elapsed=elapsed
        )

    def ask_str(self, prompt: str) -> str:
        """
        ====================================================================
         Send a text prompt and return only the text response.
        ====================================================================
        """
        response = self._model.generate_content(prompt)
        return response.text
