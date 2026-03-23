# Gemini

## Purpose
Client wrapper for Google Gemini API via Vertex AI.
Sends text prompts and returns structured responses with metadata.
Configurable model (default: gemini-2.5-flash).

## Public API

### `__init__(creds: SACredentials, model: str = None, location: str = 'us-central1') -> None`
Create a Gemini client with SA credentials.
- `model`: Gemini model name (default `gemini-2.5-flash`)
- `location`: Google Cloud region (default `us-central1`)

### `ask(prompt: str) -> ResponseGemini`
Send a text prompt and return a structured response.
- Returns `ResponseGemini` with `.text`, `.model`, `.input_tokens`,
  `.output_tokens`, `.total_tokens`, `.finish_reason`

## Inheritance (Hierarchy)
```
Gemini (no base class)
```
Standalone client wrapper.

## Dependencies

| Import | Purpose |
|--------|---------|
| `vertexai` | Vertex AI initialization |
| `vertexai.generative_models.GenerativeModel` | Gemini model |
| `google.oauth2.service_account.Credentials` | SA credentials |
| `ResponseGemini` | Structured response type |

## Usage Example
```python
from f_google.services.gemini import Gemini

# Default model (gemini-2.5-flash)
gemini = Gemini.Factory.rami()
response = gemini.ask(prompt='Explain A* algorithm')
print(response.text)
print(response.total_tokens)

# Specific model
gemini = Gemini.Factory.rami(model='gemini-2.5-pro')
response = gemini.ask(prompt='Summarize this paper')
print(repr(response))
# ResponseGemini(model=gemini-2.5-pro, tokens=150, finish=STOP)
```
