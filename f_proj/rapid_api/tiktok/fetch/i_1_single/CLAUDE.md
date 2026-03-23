# FetchSingle

## Purpose
Fetch a single item from TikTok RapidAPI and convert it via a
caller-provided `to_row` function.

## Public API

| Method | Signature | Description |
|--------|-----------|-------------|
| `run` | `(url, params, anchor, to_row) -> list[dict]` | Fetch single item |

## Inheritance
`FetchSingle` -> `FetchBase` (inherits config and helpers).

## Dependencies
- `f_proj.rapid_api.tiktok.fetch.i_0_base.FetchBase`
