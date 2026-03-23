# FetchMulti

## Purpose
Fetch multiple items (paginated) from TikTok RapidAPI. Manages
cursor-based pagination via the internal `_batch.Batch` dataclass.
Accepts `to_row` (singular) and handles list iteration, status
stamping, and optional early termination via `stop_if`.

## Public API

| Method | Signature | Description |
|--------|-----------|-------------|
| `run` | `(url, params, anchor, name_list, to_row, name_cursor, limit, stop_if) -> list[dict]` | Paginated fetch |

## Internal Files
- `_batch.py` — `Batch` dataclass (pagination state: items, has_more, cursor)

## Inheritance
`FetchMulti` -> `FetchBase` (inherits config and helpers).

## Dependencies
- `f_proj.rapid_api.tiktok.fetch.i_0_base.FetchBase`
