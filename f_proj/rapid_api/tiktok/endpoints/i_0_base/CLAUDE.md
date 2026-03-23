# Endpoint

## Purpose
Base class for all TikTok API endpoints. Owns the `run()` dispatch
logic — subclasses define only config and field mapping.

## Public API

| Method | Signature | Description |
|--------|-----------|-------------|
| `run` | `(limit?) -> list[dict]` | Execute the endpoint fetch |
| `_params` | `() -> dict` | Build API params (override) |
| `_anchor` | `() -> tuple` | Return request anchor (override) |
| `_to_row` | `(item: dict) -> dict` | Map response item to row (override) |

## Config Attributes

| Attribute | Type | Default | Description |
|-----------|------|---------|-------------|
| `_path` | `str` | — | API endpoint path |
| `_name_list` | `str` | `None` | Response list key (None = single fetch) |
| `_name_cursor` | `str` | `'cursor'` | Cursor field name |
| `_stop_if` | `Callable` | `None` | Override as method for early termination |

## Inheritance
No base class (root of endpoint hierarchy).

## Dependencies
- `f_proj.rapid_api.tiktok.fetch.i_0_base.FetchBase`
- `f_proj.rapid_api.tiktok.fetch.i_1_single.FetchSingle`
- `f_proj.rapid_api.tiktok.fetch.i_1_multi.FetchMulti`
