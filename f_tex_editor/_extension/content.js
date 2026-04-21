// f_tex_editor content script — auto-redirect Drive .tex preview
// pages into the local editor.
//
// Runs on https://drive.google.com/file/d/<id>/view*. The preview
// URL does not expose the filename; we read it from document.title
// (populated asynchronously by Drive's JS) and redirect once we
// confirm it's a .tex file. A dark overlay hides Drive's empty
// "No preview available" page during the brief detection window.

(function () {
  const EDITOR = 'http://127.0.0.1:5000/drive-ui/open?fileId=';

  const m = location.pathname.match(/\/file\/d\/([^/]+)/);
  if (!m) return;
  const fileId = m[1];

  // ── Overlay ──────────────────────────────────────────────────
  const overlay = document.createElement('div');
  overlay.id = '__ftex_overlay';
  overlay.setAttribute(
    'style',
    'position:fixed;inset:0;z-index:2147483647;' +
    'background:#1e1e1e;color:#ddd;' +
    'display:flex;align-items:center;justify-content:center;' +
    'font:14px system-ui,sans-serif;'
  );
  overlay.textContent = 'f_tex_editor — checking file type…';

  function installOverlay() {
    const root = document.documentElement;
    if (root) {
      root.appendChild(overlay);
    } else {
      setTimeout(installOverlay, 5);
    }
  }
  installOverlay();

  // ── Detection ────────────────────────────────────────────────
  // Drive's title format is "<filename> - Google Drive" (or just
  // "<filename>" briefly during load). We extract the filename
  // portion and check it ends with .tex / .latex — strict enough
  // to avoid matching on compiled .pdf siblings like "foo.tex.pdf".
  function isTex() {
    const title = document.title || '';
    const filename = title.split(' - ')[0].trim();
    return /\.(tex|latex)$/i.test(filename);
  }

  function redirect() {
    location.replace(EDITOR + encodeURIComponent(fileId));
  }

  // Fast path: title already populated (e.g., back/forward nav).
  if (isTex()) return redirect();

  // Slow path: poll until the title populates, up to 2.5s.
  const DEADLINE = Date.now() + 2500;
  const timer = setInterval(() => {
    if (isTex()) {
      clearInterval(timer);
      redirect();
    } else if (Date.now() > DEADLINE) {
      clearInterval(timer);
      overlay.remove();
    }
  }, 50);
})();
