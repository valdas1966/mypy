# f_tex_editor

## Purpose
Browser-based LaTeX editor: Monaco source editor on the left, PDF
preview (iframe) on the right. Wraps a Flask server that reads/writes
local `.tex` files and compiles them via `f_tex.Tex`.

Phase 1 target: **localhost only**, single-file editing. Drive open/save
(Phase 2), Cloudflare Tunnel (Phase 3), and Google Cloud Drive-UI
integration (Phase 4+) are out of scope.

## Public API

### `class TexEditor`

#### `TexEditor.__init__(tex: Tex, default_path: str = '/tmp/untitled.tex') -> None`
Bind the editor to a `Tex` compiler. `default_path` is shown in the
browser when `/` is opened without a `?path=` query parameter.

#### `TexEditor.app -> Flask` *(property)*
Flask application object. Exposed for test clients
(`app.test_client()`).

#### `TexEditor.tex -> Tex` *(property)*
Underlying compiler.

#### `TexEditor.run(host='127.0.0.1', port=5000, debug=False) -> None`
Start Flask's development server. Blocks until Ctrl+C.

#### `TexEditor.__repr__() -> str`
`TexEditor(tex=Tex(engine='tectonic'))`-style repr.

### HTTP Routes

| Route | Method | Behavior |
|-------|--------|----------|
| `/` | GET | Serve the Monaco + iframe HTML page. |
| `/file?path=<p>` | GET | Read file; JSON `{path, src}`. Missing file returns `src=''`. Missing `path` returns 400. |
| `/save` | POST | JSON `{path, src}`. Writes src to disk, compiles via `Tex.compile_file`, caches PDF bytes by path. Returns `{ok, bytes}` or `{ok: false, error}`. |
| `/pdf?path=<p>` | GET | Serve the most recent PDF for `path`. 404 if nothing compiled yet. |

## Inheritance (Hierarchy)
```
TexEditor   (no base class)
```
Standalone class. Holds a `Tex` (composition, not inheritance) and a
Flask `app`.

## Dependencies

| Import | Category | Used for |
|--------|----------|----------|
| `flask.Flask` / routing helpers | third-party | HTTP server |
| `pathlib.Path` | stdlib | file I/O |
| `io.BytesIO` | stdlib | `send_file` over in-memory PDF |
| `f_tex.Tex` | framework | LaTeX compilation |
| `pytest` | third-party | `_tester.py` only |

Frontend (loaded via CDN, not a Python dep):
- Monaco Editor 0.45.0 — source editor.
- Browser-native PDF viewer — preview.

## Usage Example

```python
from f_tex_editor import TexEditor

editor = TexEditor.Factory.a()
editor.run()  # http://127.0.0.1:5000/?path=/tmp/foo.tex
```

Or launch via the included script:

```bash
python -m f_tex_editor.s_run
```

Then open `http://127.0.0.1:5000/?path=/tmp/my_doc.tex` in a browser.
The file is created on first save.

## File Layout
```
f_tex_editor/
├── main.py              # TexEditor class + Flask routes
├── _factory.py          # Factory.a() -> default TexEditor
├── _tester.py           # pytest — Flask test_client based
├── __init__.py          # exports TexEditor; wires Factory
├── _assets/
│   └── index.html       # Monaco + iframe PDF UI
├── s_run.py             # launcher: TexEditor.Factory.a().run()
└── CLAUDE.md            # this file
```

## Design Notes

1. **Compile on save** (Ctrl+S), not on keystroke — predictable, no
   queue build-up with slow compiles.
2. **PDF served from in-memory cache** keyed by file path — no `/tmp`
   PDF pollution, scales to multi-tab editing.
3. **`compile_file` over `compile(src)`** — lets multi-file projects
   (`\input{..}`, figures, bib) resolve relative to the .tex file's
   directory.
4. **iframe PDF viewer** (browser native) — no pdf.js dep. Scroll
   position resets on recompile; acceptable for Phase 1.
5. **Monaco loaded from unpkg CDN** — Phase 1 simplicity. Vendor
   locally if CSP/offline becomes a requirement.
6. **Hello-world seed for missing/empty files** — when `/file`
   returns `src=''`, the frontend preseeds Monaco with a minimal
   compilable `\documentclass{article} ... \end{document}` so that
   the first Ctrl+S produces a valid PDF instead of tectonic's
   `no legal \end found` error. Non-empty existing files are not
   touched.
