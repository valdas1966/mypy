import json
from io import BytesIO
from pathlib import Path, PurePosixPath
from typing import TYPE_CHECKING

from flask import (
    Flask, Response, jsonify, redirect, request, send_file,
)

from f_tex import Tex

if TYPE_CHECKING:
    from f_google.services.drive import Drive


class TexEditor:
    """
    ============================================================================
     TexEditor — browser-based LaTeX editor.
     Monaco on the left, iframe PDF preview on the right, served by Flask.
     Ctrl+S saves the source to disk and recompiles via f_tex.Tex.
     Local mode: ?path=<local>. Drive mode: ?drive=<Drive path>, using
     Drive.Factory.valdas() lazily (no OAuth cost until first Drive request).
    ============================================================================
    """

    # Factory
    Factory: type = None

    _ASSETS = Path(__file__).parent / '_assets'
    _DRIVE_CACHE_DIR: Path = Path('/tmp/drive-cache')

    def __init__(self,
                 tex: Tex,
                 default_path: str = '/tmp/untitled.tex',
                 drive: 'Drive | None' = None) -> None:
        """
        ========================================================================
         Init TexEditor with a Tex Compiler.
         default_path is loaded when the browser opens '/' without a ?path.
         drive is optional (injected for tests); if None, lazy-init via
         Drive.Factory.valdas() on first Drive request.
        ========================================================================
        """
        self._tex = tex
        self._default_path = default_path
        self._pdf_cache: dict[str, bytes] = {}
        self._drive = drive
        self._app = self._build_app()

    @property
    def app(self) -> Flask:
        """
        ========================================================================
         Flask Application (useful for test clients).
        ========================================================================
        """
        return self._app

    @property
    def tex(self) -> Tex:
        """
        ========================================================================
         Underlying Tex Compiler.
        ========================================================================
        """
        return self._tex

    @property
    def drive(self) -> 'Drive':
        """
        ========================================================================
         Drive client (lazy-initialized via Drive.Factory.valdas() on
         first access; avoids OAuth cost for pure-local-mode sessions).
        ========================================================================
        """
        if self._drive is None:
            from f_google.services.drive import Drive
            self._drive = Drive.Factory.valdas()
        return self._drive

    def run(self,
            host: str = '127.0.0.1',
            port: int = 5000,
            debug: bool = False) -> None:
        """
        ========================================================================
         Start the Flask Development Server (blocks until Ctrl+C).
        ========================================================================
        """
        self._app.run(host=host, port=port, debug=debug)

    def _build_app(self) -> Flask:
        """
        ========================================================================
         Build the Flask App and register all routes.
        ========================================================================
        """
        app = Flask(import_name=__name__)
        app.add_url_rule('/', view_func=self._route_index)
        app.add_url_rule('/file', view_func=self._route_file)
        app.add_url_rule('/save',
                         view_func=self._route_save,
                         methods=['POST'])
        app.add_url_rule('/pdf', view_func=self._route_pdf)
        app.add_url_rule('/drive/open',
                         view_func=self._route_drive_open)
        app.add_url_rule('/drive/save',
                         view_func=self._route_drive_save,
                         methods=['POST'])
        app.add_url_rule('/drive/pdf',
                         view_func=self._route_drive_pdf)
        app.add_url_rule('/drive-ui/open',
                         view_func=self._route_drive_ui_open)
        return app

    def _route_index(self) -> Response:
        """
        ========================================================================
         GET / - serve the Monaco + iframe-PDF page.
        ========================================================================
        """
        html = (self._ASSETS / 'index.html').read_text(encoding='utf-8')
        html = html.replace('__DEFAULT_PATH__', self._default_path)
        return Response(response=html, mimetype='text/html')

    def _route_file(self) -> Response:
        """
        ========================================================================
         GET /file?path=... - read the file's UTF-8 source.
         Returns src='' if the file does not exist (create-on-save model).
        ========================================================================
        """
        path = request.args.get(key='path', default='')
        if not path:
            return jsonify({'error': 'missing path'}), 400
        p = Path(path)
        src = p.read_text(encoding='utf-8') if p.is_file() else ''
        return jsonify({'path': str(p), 'src': src})

    def _route_save(self) -> Response:
        """
        ========================================================================
         POST /save {path, src} - write src to disk and recompile.
         On success: cache PDF bytes by path and return {ok: True}.
         On failure: return {ok: False, error: <engine stderr>}.
        ========================================================================
        """
        data = request.get_json(force=True, silent=True) or {}
        path = data.get('path', '')
        src = data.get('src', '')
        if not path:
            return jsonify({'ok': False, 'error': 'missing path'}), 400
        p = Path(path)
        p.parent.mkdir(parents=True, exist_ok=True)
        p.write_text(data=src, encoding='utf-8')
        try:
            # compile_file lets multi-file \input{..} resolve from p.parent
            pdf = self._tex.compile_file(path_src=str(p))
        except RuntimeError as e:
            return jsonify({'ok': False, 'error': str(e)})
        self._pdf_cache[str(p)] = pdf
        return jsonify({'ok': True, 'bytes': len(pdf)})

    def _route_pdf(self) -> Response:
        """
        ========================================================================
         GET /pdf?path=... - serve the most-recently-compiled PDF for path.
         Returns 404 if nothing has been compiled yet for that path.
        ========================================================================
        """
        path = request.args.get(key='path', default='')
        key = str(Path(path))
        if key not in self._pdf_cache:
            return Response(response=b'', status=404)
        return send_file(
            path_or_file=BytesIO(self._pdf_cache[key]),
            mimetype='application/pdf',
            download_name='preview.pdf',
        )

    def _route_drive_open(self) -> Response:
        """
        ========================================================================
         GET /drive/open?drive=<path>|?fileId=<id> - download the Drive
         file to local cache and return its UTF-8 source.
         `fileId` is resolved to a path via Drive.get_path_by_id; the
         resolved path is echoed back as `drivePath` so the browser can
         save against the path (not the id) afterwards.
         Missing file on Drive returns src='' (create-on-save model).
        ========================================================================
        """
        drive_path = request.args.get(key='drive', default='').strip()
        file_id = request.args.get(key='fileId', default='').strip()
        if not drive_path and not file_id:
            return jsonify({'ok': False,
                            'error': 'missing drive or fileId'}), 400
        if file_id and not drive_path:
            try:
                drive_path = self.drive.get_path_by_id(file_id=file_id)
            except FileNotFoundError as e:
                return jsonify({'ok': False, 'error': str(e)}), 404
        try:
            safe = self._drive_safe_path(drive_path=drive_path)
        except ValueError as e:
            return jsonify({'ok': False, 'error': str(e)}), 400
        local = self._drive_local(drive_path=safe)
        try:
            if self.drive.is_exists(path=safe):
                local.parent.mkdir(parents=True, exist_ok=True)
                self.drive.download(path_src=safe,
                                    path_dest=str(local))
                src = local.read_text(encoding='utf-8')
            else:
                src = ''
        except Exception as e:
            return jsonify({'ok': False,
                            'error': f'Drive: {e}'}), 500
        return jsonify({'ok': True,
                        'drivePath': safe,
                        'localPath': str(local),
                        'src': src})

    def _route_drive_save(self) -> Response:
        """
        ========================================================================
         POST /drive/save {drivePath|fileId, src} - write to cache,
         compile, upload both .tex and .pdf to Drive.
         `fileId` is resolved to a drivePath via Drive.get_path_by_id.
         driveUploaded=False if compile succeeded but upload failed.
        ========================================================================
        """
        data = request.get_json(force=True, silent=True) or {}
        drive_path = (data.get('drivePath') or '').strip()
        file_id = (data.get('fileId') or '').strip()
        src = data.get('src', '')
        if not drive_path and not file_id:
            return jsonify({'ok': False,
                            'error': 'missing drivePath or fileId'
                            }), 400
        if file_id and not drive_path:
            try:
                drive_path = self.drive.get_path_by_id(file_id=file_id)
            except FileNotFoundError as e:
                return jsonify({'ok': False, 'error': str(e)}), 404
        try:
            safe = self._drive_safe_path(drive_path=drive_path)
        except ValueError as e:
            return jsonify({'ok': False, 'error': str(e)}), 400
        local_tex = self._drive_local(drive_path=safe)
        local_tex.parent.mkdir(parents=True, exist_ok=True)
        local_tex.write_text(data=src, encoding='utf-8')
        # Compile
        try:
            pdf = self._tex.compile_file(path_src=str(local_tex))
        except RuntimeError as e:
            return jsonify({'ok': False, 'error': str(e)})
        self._pdf_cache[self._drive_cache_key(drive_path=safe)] = pdf
        # Upload .tex and .pdf (the .pdf is written next to the .tex
        # for a clean local mirror, then uploaded as a sibling).
        pdf_drive_path = str(
            PurePosixPath(safe).with_suffix('.pdf'))
        local_pdf = local_tex.with_suffix('.pdf')
        local_pdf.write_bytes(pdf)
        try:
            self.drive.upload(path_src=str(local_tex),
                              path_dest=safe)
            self.drive.upload(path_src=str(local_pdf),
                              path_dest=pdf_drive_path)
        except Exception as e:
            return jsonify({'ok': True,
                            'bytes': len(pdf),
                            'drivePath': safe,
                            'driveUploaded': False,
                            'driveError': f'Drive upload failed: {e}'})
        return jsonify({'ok': True,
                        'bytes': len(pdf),
                        'drivePath': safe,
                        'drivePdfPath': pdf_drive_path,
                        'driveUploaded': True})

    def _route_drive_pdf(self) -> Response:
        """
        ========================================================================
         GET /drive/pdf?drive=<path>|?fileId=<id> - serve the cached PDF
         for the most recent Drive-mode compile.
        ========================================================================
        """
        drive_path = request.args.get(key='drive', default='').strip()
        file_id = request.args.get(key='fileId', default='').strip()
        if not drive_path and not file_id:
            return Response(response=b'', status=404)
        if file_id and not drive_path:
            try:
                drive_path = self.drive.get_path_by_id(file_id=file_id)
            except FileNotFoundError:
                return Response(response=b'', status=404)
        try:
            safe = self._drive_safe_path(drive_path=drive_path)
        except ValueError:
            return Response(response=b'', status=400)
        key = self._drive_cache_key(drive_path=safe)
        if key not in self._pdf_cache:
            return Response(response=b'', status=404)
        return send_file(
            path_or_file=BytesIO(self._pdf_cache[key]),
            mimetype='application/pdf',
            download_name='preview.pdf',
        )

    def _route_drive_ui_open(self) -> Response:
        """
        ========================================================================
         GET /drive-ui/open - entry point from a Drive-side trigger.
         Accepts either:
           ?fileId=<id>          (bookmarklet / Chrome extension)
           ?state=<url-JSON>     (future Drive UI Integration payload,
                                  shape: {"ids":["<id>"],"action":"open"})
         Extracts the fileId and 302-redirects to /?fileId=<id>.
         The editor SPA then resolves the fileId via /drive/open?fileId.
        ========================================================================
        """
        file_id = request.args.get(key='fileId', default='').strip()
        state_raw = request.args.get(key='state', default='').strip()
        if state_raw and not file_id:
            try:
                state = json.loads(state_raw)
            except Exception as e:
                return Response(
                    response=f'Bad state JSON: {e}'.encode(),
                    status=400,
                )
            ids = state.get('ids') or []
            if ids:
                file_id = str(ids[0]).strip()
        if not file_id:
            return Response(
                response=b'Missing fileId or state.',
                status=400,
            )
        return redirect(
            location=f'/?fileId={file_id}',
            code=302,
        )

    @staticmethod
    def _drive_safe_path(drive_path: str) -> str:
        """
        ========================================================================
         Reject absolute paths and parent-references. Return the
         normalized POSIX path string.
        ========================================================================
        """
        p = PurePosixPath(drive_path)
        if p.is_absolute() or '..' in p.parts:
            raise ValueError(f'Unsafe drive path: {drive_path!r}')
        return str(p)

    def _drive_local(self, drive_path: str) -> Path:
        """
        ========================================================================
         Map a Drive path to its /tmp/drive-cache local mirror.
        ========================================================================
        """
        return self._DRIVE_CACHE_DIR / drive_path

    @staticmethod
    def _drive_cache_key(drive_path: str) -> str:
        """
        ========================================================================
         Cache key for a Drive-mode PDF; prefix avoids collision with
         local-mode keys in the same _pdf_cache dict.
        ========================================================================
        """
        return f'drive:{drive_path}'

    def __repr__(self) -> str:
        return f'TexEditor(tex={self._tex!r})'
