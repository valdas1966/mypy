from io import BytesIO
from pathlib import Path

from flask import Flask, Response, jsonify, request, send_file

from f_tex import Tex


class TexEditor:
    """
    ============================================================================
     TexEditor — browser-based LaTeX editor.
     Monaco on the left, iframe PDF preview on the right, served by Flask.
     Ctrl+S saves the source to disk and recompiles via f_tex.Tex.
     Phase 1: local files only (no Drive, no tunnel, no OAuth).
    ============================================================================
    """

    # Factory
    Factory: type = None

    _ASSETS = Path(__file__).parent / '_assets'

    def __init__(self,
                 tex: Tex,
                 default_path: str = '/tmp/untitled.tex') -> None:
        """
        ========================================================================
         Init TexEditor with a Tex Compiler.
         default_path is loaded when the browser opens '/' without a ?path.
        ========================================================================
        """
        self._tex = tex
        self._default_path = default_path
        self._pdf_cache: dict[str, bytes] = {}
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

    def __repr__(self) -> str:
        return f'TexEditor(tex={self._tex!r})'
