from f_psl.file.i_2_tex import FileTex


def test_add_document_class() -> None:
    """
    ========================================================================
     Test add_document_class() method.
    ========================================================================
    """
    f = FileTex.Factory.empty()
    f.add_document_class(name='article')
    assert f.lines() == ['\\documentclass{article}']
    f.delete()


def test_add_environment() -> None:
    """
    ========================================================================
     Test add_environment() method.
    ========================================================================
    """
    # Build minimal document from scratch
    f = FileTex.Factory.empty()
    f.add_document_class(name='article')
    f.add_environment(name='document')
    assert f.lines() == ['\\documentclass{article}',
                         '\\begin{document}',
                         '\\end{document}']
    f.delete()


def test_add_environment_inside_document() -> None:
    """
    ========================================================================
     Test add_environment() inserts before end of document.
    ========================================================================
    """
    f = FileTex.Factory.article()
    f.add_environment(name='itemize')
    assert f.lines() == ['\\documentclass{article}',
                          '\\begin{document}',
                          '\\begin{itemize}',
                          '\\end{itemize}',
                          '\\end{document}']
    f.delete()
