# ResponseGemini

## Purpose
Dataclass holding a Gemini API response — generated text and metadata
(model name, token counts, finish reason).

## Public API

| Signature | Behavior |
|-----------|----------|
| `ResponseGemini(text, model, input_tokens, output_tokens, finish_reason)` | Dataclass constructor. |
| `text: str` | Generated text response. |
| `model: str` | Model name used (e.g. `gemini-2.5-flash`). |
| `input_tokens: int` | Number of input (prompt) tokens. |
| `output_tokens: int` | Number of output (response) tokens. |
| `finish_reason: str` | Why generation stopped (e.g. `STOP`). |
| `total_tokens -> int` | Computed property: `input_tokens + output_tokens`. |
| `__repr__() -> str` | `'ResponseGemini(model=..., tokens=30, finish=STOP)'` |

## Inheritance (Hierarchy)
```
ResponseGemini (dataclass, no base class)
```

## Dependencies

None — pure Python.

## Usage Example
```python
from f_google.services.gemini import Gemini

response = Gemini.Factory.rami().ask(prompt='Hello')
print(response.text)
print(response.total_tokens)
print(repr(response))

# Factory (for tests)
from f_google.services.gemini.response import ResponseGemini
r = ResponseGemini.Factory.gen(text='test', input_tokens=5)
assert r.total_tokens == 25
```
