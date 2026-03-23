# ResponsePdf

## Purpose
Dataclass holding parsed PDF content — extracted markdown text
and rendered page images as PNG bytes. `str()` returns the text.

## Public API

| Signature | Behavior |
|-----------|----------|
| `ResponsePdf(text: str, pages: list[bytes])` | Dataclass constructor. |
| `text: str` | Extracted markdown (text + tables). |
| `pages: list[bytes]` | Rendered page images as PNG bytes. |
| `__repr__() -> str` | `'ResponsePdf(chars=1234, pages=5)'` |

## Inheritance (Hierarchy)
```
ResponsePdf (dataclass, no base class)
```
Standalone data container.

## Dependencies

None — pure Python, no external imports.

## Usage Example
```python
from f_pdf import UPdf, ResponsePdf

# Via UPdf
response = UPdf.read(data=pdf_bytes)
print(response.text)
print(len(response.pages))

# Via Factory (for tests)
response = ResponsePdf.Factory.gen(text='test', nr_pages=2)
assert response.text == 'test'
assert len(response.pages) == 2
```
