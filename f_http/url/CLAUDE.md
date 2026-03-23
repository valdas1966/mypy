# UUrl

## Purpose
Static utility for extracting file suffixes from URLs. Tries path
first, falls back to `mime_type`/`mimeType` query param.

## Public API

| Method | Signature | Description |
|--------|-----------|-------------|
| `suffix` | `(url: str) -> str \| None` | File extension without dot |

## Inheritance
No base class. Static utility — no instantiation.

## Dependencies
- `urllib.parse` (stdlib)

## Usage Example
```python
from f_http.url import UUrl

UUrl.suffix(url='https://cdn.example.com/video.mp4')  # 'mp4'
UUrl.suffix(url='https://cdn.example.com/stream?mime_type=video_mp4')  # 'mp4'
UUrl.suffix(url='https://example.com/no-extension')  # None
```
