# Log Package

## Purpose
Logging utilities: configuration (`u_log`) and colored console
output (`color_log`). Console logs are auto-colored — metadata
(level tag, timestamp) is colored automatically by `_ColorFormatter`.

## Package Exports

```python
from f_log import setup_log, get_log
from f_log.color_log import ColorLog
```

## Module Hierarchy

```
f_log/
├── __init__.py        re-exports setup_log, get_log
├── u_log.py           Settings, _ColorFormatter, setup_log(), get_log()
└── color_log.py       ColorLog — ANSI coloring for log message parts
```

## Module Summary

| Module | Purpose |
|--------|---------|
| `u_log` | Configure root logger (console/file/both), auto-colored console |
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
