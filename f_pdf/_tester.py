import pytest
from f_pdf.response import ResponsePdf


@pytest.fixture
def gen() -> ResponsePdf:
    """
    ========================================================================
     Create a ResponsePdf test instance.
    ========================================================================
    """
    return ResponsePdf.Factory.gen(text='Hello PDF',
                                   nr_pages=3)


def test_text(gen: ResponsePdf) -> None:
    """
    ========================================================================
     Test the text property.
    ========================================================================
    """
    assert gen.text == 'Hello PDF'


def test_pages(gen: ResponsePdf) -> None:
    """
    ========================================================================
     Test the pages property.
    ========================================================================
    """
    assert len(gen.pages) == 3


def test_repr(gen: ResponsePdf) -> None:
    """
    ========================================================================
     Test __repr__ returns debug info.
    ========================================================================
    """
    assert 'ResponsePdf' in repr(gen)
    assert 'chars=9' in repr(gen)
    assert 'pages=3' in repr(gen)
