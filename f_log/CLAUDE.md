# Log Package

## Purpose
Logging utilities: configuration (`u_log`) and colored console
output (`color_log`). Console logs are auto-colored — metadata
(level tag, timestamp) is colored automatically by `_ColorFormatter`.

## Package Exports

```python
from f_log import setup_log, get_log, log_func
from f_log.color_log import ColorLog
```

## Module Hierarchy

```
f_log/
├── __init__.py        re-exports setup_log, get_log, log_func
├── u_log.py           Settings, _ColorFormatter, setup_log(), get_log()
├── u_decorator.py     log_func — decorator for function call logging
└── color_log.py       ColorLog — ANSI coloring for log message parts
```

## Module Summary

| Module | Purpose |
|--------|---------|
| `u_log` | Configure root logger (console/file/both), auto-colored console |
| `u_decorator` | `log_func` decorator — logs func name, args, elapsed, output |
| `color_log` | Wrap text with ANSI 24-bit colors for dark terminals |

## Auto-Colored Metadata

Console output automatically colors:
- `[LEVEL]` — level name in cyan, brackets in gray
- `[timestamp]` — timestamp in amber, brackets in gray

No configuration needed — `setup_log()` uses `_ColorFormatter` for
console handlers by default.

## ColorLog API

```python
ColorLog.label(text) -> str   # Soft cyan — identifiers, keys
ColorLog.value(text) -> str   # Light green — numbers, results
ColorLog.time(text) -> str    # Warm amber — durations, timestamps
ColorLog.path(text) -> str    # Soft violet — file paths, URLs
ColorLog.warn(text) -> str    # Coral red — inline warnings
ColorLog.dim(text) -> str     # Gray — separators, low-priority
```

All methods accept `object` and return ANSI-wrapped `str`.
Colors are defined in `f_color/rgb/_colors.py` (`LOG_*` entries).

## log_func Decorator

Decorator that logs entry and exit of a function at DEBUG level.

**Entry log**: `func_name | dt_start | arg1=val1, arg2=val2`
**Exit log**: `func_name | elapsed | -> output`
**Error log**: `func_name | elapsed | !! ExcType: message`

- Skips `self` and `cls` parameters
- Truncates arg values (50 chars) and output (100 chars)
- Uses ColorLog: name=cyan, time=amber, args=gray/green, error=red
- Uses logger from `func.__module__`

```python
from f_log import setup_log, log_func

setup_log(sink='console', level=logging.DEBUG)

@log_func
def search(rows: int, k: int) -> list:
    ...
```

## Dependencies

| Import | Used By | Purpose |
|--------|---------|---------|
| `logging` | u_log | Standard library logging |
| `f_log.color_log.ColorLog` | _ColorFormatter | Auto-color metadata |
| `f_color.rgb._colors._CUSTOM` | ColorLog | LOG_* color definitions |

## Usage Example

```python
from f_log import setup_log, get_log
from f_log.color_log import ColorLog as cl

setup_log(sink='console')
log = get_log(__name__)

# Metadata auto-colored, message parts manually colored
log.info(f'{cl.label("Users")} loaded: {cl.value(150)} in {cl.time("1.2s")}')
log.info(f'{cl.path("/data/file.csv")} {cl.warn("not found")}')
```
