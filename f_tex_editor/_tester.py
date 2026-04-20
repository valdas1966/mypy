from pathlib import Path

from f_tex import Tex
from f_tex_editor import TexEditor
from f_tex_editor.main import TexEditor as _TexEditor


_HELLO = (
    r'\documentclass{article}'
    '\n'
    r'\begin{document}'
    '\n'
    r'Hello, editor.'
    '\n'
    r'\end{document}'
    '\n'
)


class _FakeDrive:
    """
    ============================================================================
     In-memory Drive double: is_exists / download / upload only.
     Storage is a {drive_path: bytes} dict.
    ============================================================================
    """

    def __init__(self,
                 fail_upload: bool = False) -> None:
        self.store: dict[str, bytes] = {}
        self._fail_upload = fail_upload

    def is_exists(self, path: str) -> bool:
        return path in self.store

    def download(self, path_src: str, path_dest: str) -> None:
        if path_src not in self.store:
            raise FileNotFoundError(path_src)
        dest = Path(path_dest)
        dest.parent.mkdir(parents=True, exist_ok=True)
        dest.write_bytes(self.store[path_src])

    def upload(self, path_src: str, path_dest: str) -> None:
        if self._fail_upload:
            raise RuntimeError('simulated upload failure')
        self.store[path_dest] = Path(path_src).read_bytes()


def _client():
    """
    ============================================================================
     Build a TexEditor and return (editor, flask_test_client).
    ============================================================================
    """
    editor = TexEditor.Factory.a()
    editor.app.config['TESTING'] = True
    return editor, editor.app.test_client()


def _drive_client(fail_upload: bool = False):
    """
    ============================================================================
     TexEditor wired to a fake Drive. Returns (editor, client, fake_drive).
    ============================================================================
    """
    fake = _FakeDrive(fail_upload=fail_upload)
    editor = _TexEditor(tex=Tex.Factory.a(), drive=fake)
    editor.app.config['TESTING'] = True
    return editor, editor.app.test_client(), fake


def test_index_returns_monaco_page() -> None:
    """
    ========================================================================
     GET / returns HTML that references the Monaco editor.
    ========================================================================
    """
    _, client = _client()
    r = client.get('/')
    assert r.status_code == 200
    assert b'monaco' in r.data.lower()


def test_index_injects_default_path() -> None:
    """
    ========================================================================
     GET / substitutes the editor's default_path placeholder.
    ========================================================================
    """
    _, client = _client()
    r = client.get('/')
    assert b'/tmp/untitled.tex' in r.data
    assert b'__DEFAULT_PATH__' not in r.data


def test_file_missing_returns_empty_src(tmp_path: Path) -> None:
    """
    ========================================================================
     GET /file on a non-existent path returns src=''.
    ========================================================================
    """
    _, client = _client()
    p = tmp_path / 'new.tex'
    r = client.get('/file', query_string={'path': str(p)})
    assert r.status_code == 200
    body = r.get_json()
    assert body['src'] == ''
    assert body['path'] == str(p)


def test_file_existing_returns_contents(tmp_path: Path) -> None:
    """
    ========================================================================
     GET /file on an existing path returns its UTF-8 contents.
    ========================================================================
    """
    _, client = _client()
    p = tmp_path / 'has.tex'
    p.write_text(data=_HELLO, encoding='utf-8')
    r = client.get('/file', query_string={'path': str(p)})
    assert r.get_json()['src'] == _HELLO


def test_file_missing_path_arg_is_400() -> None:
    """
    ========================================================================
     GET /file without ?path= returns 400.
    ========================================================================
    """
    _, client = _client()
    r = client.get('/file')
    assert r.status_code == 400


def test_save_writes_disk_and_compiles(tmp_path: Path) -> None:
    """
    ========================================================================
     POST /save writes src to disk, compiles, returns ok=True.
    ========================================================================
    """
    _, client = _client()
    p = tmp_path / 'hello.tex'
    r = client.post('/save', json={'path': str(p), 'src': _HELLO})
    assert r.status_code == 200
    body = r.get_json()
    assert body['ok'] is True
    assert body['bytes'] > 500
    assert p.read_text(encoding='utf-8') == _HELLO


def test_save_then_pdf_returns_pdf_bytes(tmp_path: Path) -> None:
    """
    ========================================================================
     After POST /save, GET /pdf returns bytes starting with %PDF.
    ========================================================================
    """
    _, client = _client()
    p = tmp_path / 'hello.tex'
    client.post('/save', json={'path': str(p), 'src': _HELLO})
    r = client.get('/pdf', query_string={'path': str(p)})
    assert r.status_code == 200
    assert r.data[:4] == b'%PDF'


def test_save_bad_tex_returns_error(tmp_path: Path) -> None:
    """
    ========================================================================
     POST /save with invalid LaTeX returns ok=False and an error string.
    ========================================================================
    """
    _, client = _client()
    p = tmp_path / 'bad.tex'
    bad = r'\documentclass{article}' '\n' r'\badmacro{x}' '\n' r'\end'
    r = client.post('/save', json={'path': str(p), 'src': bad})
    body = r.get_json()
    assert body['ok'] is False
    assert body['error']


def test_pdf_without_prior_compile_is_404(tmp_path: Path) -> None:
    """
    ========================================================================
     GET /pdf before any compile for that path returns 404.
    ========================================================================
    """
    _, client = _client()
    p = tmp_path / 'never.tex'
    r = client.get('/pdf', query_string={'path': str(p)})
    assert r.status_code == 404


def test_save_missing_path_is_400() -> None:
    """
    ========================================================================
     POST /save without a path returns 400 ok=False.
    ========================================================================
    """
    _, client = _client()
    r = client.post('/save', json={'path': '', 'src': _HELLO})
    assert r.status_code == 400
    assert r.get_json()['ok'] is False


# ─── Drive mode ───────────────────────────────────────────────────────


def test_drive_open_missing_returns_empty_src() -> None:
    """
    ========================================================================
     GET /drive/open for a path not on Drive returns src=''.
    ========================================================================
    """
    _, client, _ = _drive_client()
    r = client.get('/drive/open',
                   query_string={'drive': 'Papers/MOSPP.tex'})
    assert r.status_code == 200
    body = r.get_json()
    assert body['ok'] is True
    assert body['src'] == ''
    assert body['drivePath'] == 'Papers/MOSPP.tex'


def test_drive_open_existing_returns_contents() -> None:
    """
    ========================================================================
     GET /drive/open for a file present on fake Drive returns its src.
    ========================================================================
    """
    _, client, fake = _drive_client()
    fake.store['Papers/MOSPP.tex'] = _HELLO.encode('utf-8')
    r = client.get('/drive/open',
                   query_string={'drive': 'Papers/MOSPP.tex'})
    body = r.get_json()
    assert body['ok'] is True
    assert body['src'] == _HELLO


def test_drive_save_compiles_and_uploads() -> None:
    """
    ========================================================================
     POST /drive/save compiles the source and uploads .tex and .pdf
     to Drive under sibling paths.
    ========================================================================
    """
    _, client, fake = _drive_client()
    r = client.post('/drive/save',
                    json={'drivePath': 'Papers/MOSPP.tex',
                          'src': _HELLO})
    assert r.status_code == 200
    body = r.get_json()
    assert body['ok'] is True
    assert body['driveUploaded'] is True
    assert body['drivePath'] == 'Papers/MOSPP.tex'
    assert body['drivePdfPath'] == 'Papers/MOSPP.pdf'
    assert 'Papers/MOSPP.tex' in fake.store
    assert 'Papers/MOSPP.pdf' in fake.store
    assert fake.store['Papers/MOSPP.pdf'][:4] == b'%PDF'


def test_drive_save_then_pdf_returns_pdf_bytes() -> None:
    """
    ========================================================================
     After /drive/save, GET /drive/pdf serves the cached PDF bytes.
    ========================================================================
    """
    _, client, _ = _drive_client()
    client.post('/drive/save',
                json={'drivePath': 'Papers/x.tex', 'src': _HELLO})
    r = client.get('/drive/pdf', query_string={'drive': 'Papers/x.tex'})
    assert r.status_code == 200
    assert r.data[:4] == b'%PDF'


def test_drive_open_missing_drive_arg_is_400() -> None:
    """
    ========================================================================
     GET /drive/open without ?drive= returns 400 ok=False.
    ========================================================================
    """
    _, client, _ = _drive_client()
    r = client.get('/drive/open')
    assert r.status_code == 400
    assert r.get_json()['ok'] is False


def test_drive_save_missing_drive_path_is_400() -> None:
    """
    ========================================================================
     POST /drive/save without drivePath returns 400 ok=False.
    ========================================================================
    """
    _, client, _ = _drive_client()
    r = client.post('/drive/save',
                    json={'drivePath': '', 'src': _HELLO})
    assert r.status_code == 400
    assert r.get_json()['ok'] is False


def test_drive_save_bad_tex_returns_error_no_upload() -> None:
    """
    ========================================================================
     POST /drive/save with invalid LaTeX returns ok=False and does
     not upload anything to Drive.
    ========================================================================
    """
    _, client, fake = _drive_client()
    bad = r'\documentclass{article}' '\n' r'\badmacro{x}' '\n' r'\end'
    r = client.post('/drive/save',
                    json={'drivePath': 'Papers/bad.tex', 'src': bad})
    body = r.get_json()
    assert body['ok'] is False
    assert body['error']
    assert 'Papers/bad.tex' not in fake.store
    assert 'Papers/bad.pdf' not in fake.store


def test_drive_pdf_without_compile_is_404() -> None:
    """
    ========================================================================
     GET /drive/pdf before any compile for that path returns 404.
    ========================================================================
    """
    _, client, _ = _drive_client()
    r = client.get('/drive/pdf', query_string={'drive': 'Papers/x.tex'})
    assert r.status_code == 404


def test_drive_unsafe_path_rejected() -> None:
    """
    ========================================================================
     Absolute paths and parent-references are rejected with 400.
    ========================================================================
    """
    _, client, _ = _drive_client()
    for bad in ['../evil.tex', '/abs/evil.tex', 'Papers/../evil.tex']:
        r = client.get('/drive/open', query_string={'drive': bad})
        assert r.status_code == 400, bad


def test_drive_save_upload_failure_reports_gracefully() -> None:
    """
    ========================================================================
     When the Drive upload raises, /drive/save still returns ok=True
     (compile succeeded) but driveUploaded=False with an error string.
    ========================================================================
    """
    _, client, fake = _drive_client(fail_upload=True)
    r = client.post('/drive/save',
                    json={'drivePath': 'Papers/fail.tex',
                          'src': _HELLO})
    body = r.get_json()
    assert body['ok'] is True
    assert body['driveUploaded'] is False
    assert 'simulated upload failure' in body['driveError']
    assert 'Papers/fail.tex' not in fake.store
