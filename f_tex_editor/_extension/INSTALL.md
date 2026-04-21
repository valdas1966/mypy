# f_tex_editor — Drive "Open with" helpers

Two zero-infra ways to jump from `drive.google.com` to the local
editor. Both hit `GET /drive-ui/open?fileId=<id>`, which 302s into
`/?fileId=<id>` and auto-loads the file via `Drive.Factory.valdas()`.

The Flask server must be running (`python -m f_tex_editor.s_run`).

---

## Option A — Chrome extension (toolbar icon + Alt+T shortcut)

1. Open `chrome://extensions/`.
2. Enable **Developer mode** (top-right toggle).
3. Click **Load unpacked** → select this folder
   (`f_tex_editor/_extension/`).
4. Pin the "f_tex_editor — Open from Drive" icon to the toolbar.

**Use it — three equivalent ways:**

1. **Double-click a `.tex` file on `drive.google.com`.**
   Drive opens its empty "No preview available" page; the
   extension's content script detects the file is a `.tex`
   (reading the filename from the tab title), shows a brief
   overlay, then auto-redirects the tab to the local editor.
   End result: double-click in Drive → editor opens with the
   file loaded.
2. **Click the extension toolbar icon** on any Drive file
   preview page. Opens the editor in a new tab.
3. **Press Alt+T** on any Drive file preview page. Same as
   (2), no clicks.

If the active tab isn't a Drive file page, the icon shows a red `!`
badge and the tooltip explains what to do.

---

## Option B — Bookmarklet

1. Create a new bookmark in the browser's bookmarks bar.
2. Name it `TeX Editor`.
3. Paste this URL as the bookmark's location:

   ```js
   javascript:(function(){var m=location.pathname.match(/\/file\/d\/([^/]+)/);if(m)location.href='http://127.0.0.1:5000/drive-ui/open?fileId='+m[1];else alert('Not a Drive file page.');})();
   ```

**Use it:** open a Drive file preview page, click the bookmark.

---

## About double-click

Method 1 above (double-click → auto-redirect) is a content-script
trick, not a native Google integration:

- Drive always routes an unregistered-type double-click to
  `/file/d/<id>/view` (the "No preview available" page).
- Our content script runs on that URL, detects a `.tex`
  filename from the page title, and redirects. The user
  perceives it as "double-click opens in f_tex_editor".

Requirements:

- The local Flask server must be running
  (`python -m f_tex_editor.s_run`). If it isn't, the auto-redirect
  succeeds but the destination tab shows `ERR_CONNECTION_REFUSED`.
- The Chrome profile must have the extension installed.
- Non-`.tex` files are unaffected: the overlay hides itself after
  2.5 s and Drive's normal preview continues.

Native Drive UI Integration (which would work on ALL browsers / in
Incognito / without the extension, and would let users set
f_tex_editor as the default app via Drive's own "Open with" menu)
still requires a public HTTPS URL, a GCP Marketplace SDK listing,
and MIME-type registration. Blocked on user owning a domain.
Tracked as Route C in `f_tex_editor/CLAUDE.md`.
