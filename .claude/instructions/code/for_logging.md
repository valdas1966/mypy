# Instruction to AI Agent (Claude Code): Logging Convention

Use `f_log` (wrapper around Python `logging` + `ColorLog`). Declare a
module-level logger and use standard levels.

```python
from f_log import get_log

_log = get_log(__name__)
_log.info(f'{cl.label("GET")} {cl.path(url)} {cl.time(elapsed)}')
```

- Module-level `_log = get_log(__name__)`.
- Standard levels: `debug`, `info`, `warning`, `error`.
- Use `ColorLog` (`cl`) helpers for formatted output.
