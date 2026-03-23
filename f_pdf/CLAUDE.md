# UPdf

## Purpose
Static PDF utility — parses PDF bytes into extracted markdown
text (text + tables) and rendered page images as PNG bytes.
Uses pymupdf4llm for text extraction and PyMuPDF for rendering.

## Public API

### `UPdf.read(data: bytes, dpi: int = 200) -> ResponsePdf` (static)
Parse PDF bytes into markdown text and rendered page images.
- `data`: raw PDF file bytes
- `dpi`: resolution for page rendering (default 200)
- Returns `ResponsePdf` with `.text` and `.pages`

## Inheritance (Hierarchy)
```
UPdf (no base class)
```
Static utility class — not instantiable.

## Dependencies

| Import | Purpose |
|--------|---------|
| `fitz` (PyMuPDF) | PDF document opening and page rendering |
| `pymupdf4llm` | PDF to markdown conversion (text + tables) |
| `ResponsePdf` | Return type for read() |

## Usage Example
```python
from f_pdf import UPdf

with open('paper.pdf', 'rb') as f:
    data = f.read()

response = UPdf.read(data=data)
print(response.text)           # extracted markdown
print(len(response.pages))     # number of pages

# Save page images for viewing
for i, page in enumerate(response.pages):
    with open(f'/tmp/page_{i}.png', 'wb') as f:
        f.write(page)
```
