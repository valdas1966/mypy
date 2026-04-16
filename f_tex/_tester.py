from pathlib import Path

import pytest

from f_tex import Tex, Templates


_HELLO_WORLD = (
    r'\documentclass{article}'
    '\n'
    r'\begin{document}'
    '\n'
    r'Hello, world.'
    '\n'
    r'\end{document}'
    '\n'
)


def test_compile_returns_pdf_bytes() -> None:
    """
    ========================================================================
     compile() returns bytes starting with the PDF header.
    ========================================================================
    """
    tex = Tex.Factory.a()
    pdf = tex.compile(src=_HELLO_WORLD)
    assert pdf[:4] == b'%PDF'
    assert len(pdf) > 500


def test_compile_raises_on_bad_source() -> None:
    """
    ========================================================================
     Invalid LaTeX raises RuntimeError with engine output.
    ========================================================================
    """
    tex = Tex.Factory.a()
    bad = r'\documentclass{article}' '\n' r'\badmacro{x}' '\n' r'\end'
    with pytest.raises(RuntimeError):
        tex.compile(src=bad)


def test_compile_file_returns_bytes(tmp_path: Path) -> None:
    """
    ========================================================================
     compile_file() compiles a .tex file and returns PDF bytes.
    ========================================================================
    """
    src = tmp_path / 'doc.tex'
    src.write_text(data=_HELLO_WORLD, encoding='utf-8')
    tex = Tex.Factory.a()
    pdf = tex.compile_file(path_src=str(src))
    assert pdf[:4] == b'%PDF'


def test_compile_file_writes_path_dest(tmp_path: Path) -> None:
    """
    ========================================================================
     compile_file() writes to path_dest when given.
    ========================================================================
    """
    src = tmp_path / 'doc.tex'
    src.write_text(data=_HELLO_WORLD, encoding='utf-8')
    dest = tmp_path / 'out.pdf'
    tex = Tex.Factory.a()
    tex.compile_file(path_src=str(src), path_dest=str(dest))
    assert dest.is_file()
    assert dest.read_bytes()[:4] == b'%PDF'


def test_compile_file_missing_src_raises(tmp_path: Path) -> None:
    """
    ========================================================================
     compile_file() raises FileNotFoundError if path_src does not exist.
    ========================================================================
    """
    tex = Tex.Factory.a()
    with pytest.raises(FileNotFoundError):
        tex.compile_file(path_src=str(tmp_path / 'missing.tex'))


def test_templates_session_summary_placeholders() -> None:
    """
    ========================================================================
     Templates.session_summary() substitutes every __FIELD__ placeholder.
    ========================================================================
    """
    src = Templates.session_summary(
        project_name='MyProj',
        date='2026-04-16',
        project_path='/mnt/f/mypy',
        body=r'\section{Purpose} Testing.',
    )
    assert '__PROJECT_NAME__' not in src
    assert '__DATE__' not in src
    assert '__PROJECT_PATH__' not in src
    assert '__BODY__' not in src
    assert 'MyProj' in src
    assert '2026-04-16' in src


def test_templates_session_summary_compiles() -> None:
    """
    ========================================================================
     Templates.session_summary() output compiles via tectonic.
    ========================================================================
    """
    tex = Tex.Factory.a()
    src = Templates.session_summary(
        project_name='Drive',
        date='2026-04-16',
        project_path='/mnt/f/mypy',
        body=(r'\section{Purpose} End-to-end template test.'
              '\n'
              r'\section{Next Steps} \unchecked Ship it.'),
    )
    pdf = tex.compile(src=src)
    assert pdf[:4] == b'%PDF'
    assert len(pdf) > 1000
