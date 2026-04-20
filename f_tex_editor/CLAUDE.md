# f_tex_editor

## Purpose
Browser-based LaTeX editor: Monaco source editor on the left, PDF
preview (iframe) on the right. Wraps a Flask server that reads/writes
`.tex` files (local or Drive) and compiles them via `f_tex.Tex`.

Phase 1 (local mode): `?path=<local>` — files read/written on local
disk. Compile + in-memory PDF preview.

Phase 2a (Drive mode — this module): `?path=<Drive path>` via
`?drive=<path>`. Download from Drive to `/tmp/drive-cache/<mirror>`,
edit in Monaco, on save compile locally and upload **both**
`.tex` and `.pdf` back to Drive (sibling paths). Auth uses the
repo-wide `Drive.Factory.valdas()` — single-user by design.

Out of scope (later phases): Cloudflare Tunnel public URL (Phase 3),
GCP OAuth app + Drive UI integration (Phases 4–6, unlocks Drive's
native "Open with" menu entry), multi-user token flows.

## Public API

### `class TexEditor`

#### `TexEditor.__init__(tex: Tex, default_path: str = '/tmp/untitled.tex', drive: Drive | None = None) -> None`
Bind the editor to a `Tex` compiler. `default_path` is shown in the
browser when `/` is opened without `?path=` / `?drive=`. `drive` is
an optional injected client (tests pass a fake); if `None`, the
editor lazy-initializes via `Drive.Factory.valdas()` on the first
Drive request.

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
| `/drive/open?drive=<p>` | GET | Download Drive path to `/tmp/drive-cache/<p>`; JSON `{ok, drivePath, localPath, src}`. Missing Drive file returns `src=''`. Unsafe path → 400. |
| `/drive/save` | POST | JSON `{drivePath, src}`. Writes to `/tmp/drive-cache`, compiles, caches PDF, uploads **both** `.tex` and `.pdf` to sibling Drive paths. Returns `{ok, bytes, drivePath, drivePdfPath, driveUploaded}`. Upload failure → `ok: true` but `driveUploaded: false` + `driveError`. |
| `/drive/pdf?drive=<p>` | GET | Serve the most recent Drive-mode PDF. 404 if nothing compiled yet for that Drive path. |

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
7. **Draggable vertical splitter** — a 6px `#splitter` column
   sits between `#editor` and `#preview`. The left column width
   is driven by a CSS variable `--left` on `#app`; drag updates
   it via mousemove. Each pane is clamped to a 200px minimum.
   Position is persisted in `localStorage` under
   `texEditor.splitLeft` and restored on page load. During drag,
   `pointer-events: none` is applied to the editor and the PDF
   iframe so the mousemove stream reaches `document` (the iframe
   otherwise swallows it). Monaco's `automaticLayout: true`
   reflows the editor during the drag with no extra wiring.
8. **PDF viewer: sidebar hidden by default** — the iframe `src`
   is suffixed with `#toolbar=1&navpanes=0&pagemode=none`.
   `navpanes=0` hides the thumbnails panel in Chromium/Edge;
   `pagemode=none` does the same in Firefox/pdf.js. `toolbar=1`
   keeps the native toolbar visible, so the user can re-open
   the thumbnails panel via the viewer's own hamburger button
   when needed. Fragment hints are per-viewer and not a W3C
   standard; if a given browser ignores them, the fallback is
   switching to pdf.js (Phase 2 concern, not done).
9. **Drive mode: path-based, `valdas`-scoped** — opt-in via
   `?drive=<Drive path>`. Single-user assumption: the editor
   acts on the `valdas` OAuth account, no per-user token flow.
   Paths (not fileIds) are the interchange format — consistent
   with the rest of `f_google.services.drive`. FileId support
   is deferred until Drive's "Open with" flow (Phase 3+) makes
   it unavoidable.
10. **Drive cache mirrors Drive tree** — `/tmp/drive-cache/<p>`
    for every Drive path `<p>`. Keeps `compile_file`'s relative
    `\input{…}` / bib resolution working once multi-file
    download lands (Phase 2b). Auxiliary files (`.aux`, `.log`,
    `.out`) are written by tectonic next to the `.tex` but are
    **never uploaded** — only `.tex` and `.pdf` go to Drive.
11. **Drive PDF cache key is namespaced** — `drive:<path>` to
    avoid collision with local-mode entries in the same
    `_pdf_cache` dict. Same dict, disjoint keys.
12. **Drive upload is best-effort, non-blocking for success** —
    if the compile succeeds but the upload raises (OAuth
    expired, network failure), `/drive/save` still returns
    `ok: true` with `driveUploaded: false` + `driveError`. The
    status bar surfaces this without losing the compile.
13. **Safe-path guard** — absolute paths and `..` components in
    `?drive=` refs are rejected with 400. Single-user localhost
    so not a security boundary — correctness guard against
    accidental cache escape when paths come from URL typos.
