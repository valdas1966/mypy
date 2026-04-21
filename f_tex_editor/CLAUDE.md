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

Phase 3a (fileId entry point — this module): `?fileId=<id>` on
every Drive route, plus a `/drive-ui/open` entry that accepts
either `?fileId=<id>` (bookmarklet / Chrome extension) or
`?state=<JSON>` (future Drive UI Integration payload). FileIds
are resolved to paths server-side via `Drive.get_path_by_id`;
the browser then reads `drivePath` from the response and uses it
for subsequent saves. This is the shared foundation for Routes A
(bookmarklet) and B (Chrome extension) under `_extension/`.

Out of scope: Cloudflare Tunnel public URL + GCP Marketplace SDK
Drive-UI Integration listing (Route C — enables native right-click
"Open with" and double-click default in Drive). Blocked on the
user owning a domain. Infrastructure, not code.

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
| `/drive/open?drive=<p>` \| `?fileId=<id>` | GET | Download the Drive file to `/tmp/drive-cache/<p>`; JSON `{ok, drivePath, localPath, src}`. `fileId` is resolved to `drivePath` via `Drive.get_path_by_id`; the resolved `drivePath` is echoed in the response. Missing file → `src=''`. Unknown `fileId` → 404. Neither param → 400. Unsafe path → 400. |
| `/drive/save` | POST | JSON `{drivePath \| fileId, src}`. Writes to `/tmp/drive-cache`, compiles, caches PDF, uploads **both** `.tex` and `.pdf` to sibling Drive paths. Returns `{ok, bytes, drivePath, drivePdfPath, driveUploaded}`. Upload failure → `ok: true` but `driveUploaded: false` + `driveError`. Unknown `fileId` → 404. |
| `/drive/pdf?drive=<p>` \| `?fileId=<id>` | GET | Serve the most recent Drive-mode PDF. 404 if nothing compiled yet, or if `fileId` is unknown. |
| `/drive-ui/open?fileId=<id>` \| `?state=<JSON>` | GET | Entry point from a Drive-side trigger (bookmarklet / extension / future Drive UI Integration). Extracts the fileId (directly or from `state.ids[0]`) and 302-redirects to `/?fileId=<id>`. Missing / malformed → 400. |

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
├── _extension/          # Chrome MV3 extension (Route B)
│   ├── manifest.json
│   ├── background.js
│   └── INSTALL.md       # setup + bookmarklet fallback
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
14. **FileId is server-resolved, browser-forgotten** — when the
    editor loads with `?fileId=<id>`, the Flask backend resolves
    it to a `drivePath` via `Drive.get_path_by_id` on the first
    `/drive/open` call and echoes `drivePath` back in the JSON.
    The frontend captures that path and uses it for every
    subsequent `/drive/save` and `/drive/pdf` call. Rationale:
    path is the interchange format everywhere else in the stack
    (`_pdf_cache` key, `/tmp/drive-cache` mirror, Drive upload
    target) — keeping fileId confined to the entry point avoids
    parallel code paths. One round-trip cost per file open.
15. **`/drive-ui/open` is the single entry for external triggers**
    — Route A (bookmarklet), Route B (Chrome extension), and the
    eventual Route C (Drive UI Integration manifest's "Open URL")
    all hit this one route. It accepts `?fileId=<id>` directly
    (A/B) or `?state=<URL-encoded JSON>` with Drive's shape
    `{"ids":["<id>"],"action":"open","userId":"..."}` (C). In
    every case it extracts the fileId and 302s into the SPA at
    `/?fileId=<id>`. One route, three delivery paths.
16. **Chrome extension is MV3, zero infrastructure** (Route B).
    `_extension/background.js` is a service worker. On toolbar
    click or `Alt+T`, it reads the active tab URL, parses the
    fileId from `/file/d/<id>/view`, and opens
    `http://127.0.0.1:5000/drive-ui/open?fileId=<id>` in a new
    tab. `host_permissions` is narrowed to `drive.google.com/*`
    and `127.0.0.1/*` — no read access to other pages. The
    extension is loaded via `chrome://extensions/` → "Load
    unpacked" — no Chrome Web Store publication needed for the
    solo-user workflow. See `_extension/INSTALL.md` for setup
    steps and the bookmarklet fallback.
17. **Content-script auto-redirect = pseudo double-click-open.**
    `_extension/content.js` runs at `document_start` on
    `drive.google.com/file/d/*/view*`. Drive always lands an
    unregistered-type double-click on that URL (there's no
    native TeX viewer), so the content script:
    - Injects a dark overlay over Drive's empty preview page
      (z-index 2147483647 — above Drive's chrome).
    - Polls `document.title` every 50 ms for up to 2.5 s. The
      title populates asynchronously as `"<filename> - Google
      Drive"`.
    - Splits on ` - ` and matches the filename against
      `/\.(tex|latex)$/i`. Strict filename match avoids false-
      positives on e.g. compiled `foo.tex.pdf` siblings.
    - On match: `location.replace(EDITOR + fileId)` — same tab,
      no Drive-preview entry in history (back button returns to
      the Drive grid).
    - On timeout / non-match: removes the overlay and lets
      Drive's preview render normally.

    Rationale for title-based detection: a content script on
    `drive.google.com` can't call Drive's API (no OAuth token
    in that origin). The filename is the only source of truth
    accessible from the page, and `<title>` is where Drive
    exposes it. Cross-origin fetch to the local Flask server
    would need CORS + a background message-passing detour —
    not worth the complexity when the title is reliable.

    Net UX: user double-clicks a `.tex` on Drive → Drive
    navigates to the preview page → content script redirects
    to the editor. From the user's perspective, double-click
    = opens in the editor. Not a native Drive integration —
    works only in Chrome profiles with the extension installed,
    and only while the local Flask server is running. The real
    native path is Route C.
