from f_core.components.data import Data, dataclass
import pytest


@pytest.fixture
def ex() -> Data:
    @dataclass
    class D(Data):
        name: str
    return D(name='abc')


def test_to_dict(ex) -> None:
    assert ex.to_dict() == {'name': 'abc'}
