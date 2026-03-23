# PipelineInsert

## Purpose
Pipeline for inserting TikTok API data into BigQuery. Maps endpoint
names to (output table, TODO table, API function) and runs parallel
fetch+insert via `_insert_parallel`.

## Public API

| Method | Signature | Description |
|--------|-----------|-------------|
| `run` | `(name: str, workers: int = 5) -> None` | Run pipeline by name |
| `names` | `() -> list[str]` | All registered pipeline names |

## Config
- `_REGISTRY` — maps name to `(tname, tname_todo, func)` tuple

## Internal Files
- `_insert_parallel.py` — generic parallel fetch+insert engine

## Inheritance
No base class.

## Dependencies
- `f_proj.rapid_api.tiktok.ApiTikTok`
- `f_proj.noteret.tiktok.tables.Tables`
- `f_google.services.bigquery.BigQuery`
- `f_core.processes.i_3_parallel.ProcessParallel`
