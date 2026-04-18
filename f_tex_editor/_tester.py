from pathlib import Path

from f_tex_editor import TexEditor


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


def _client():
    """
    ============================================================================
     Build a TexEditor and return (editor, flask_test_client).
    ============================================================================
    """
    editor = TexEditor.Factory.a()
    editor.app.config['TESTING'] = True
    return editor, editor.app.test_client()


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
