import pytest
from f_data_structure.mixins.traversable import Traversable
from f_data_structure.mixins.container_traversable import ContainerTraversable


class Container(ContainerTraversable):

    def __init__(self, indexes_non_traversable: list = list()):
        ContainerTraversable.__init__(self, elements='cells')
        self._cells = [Traversable() for _ in range(4)]
        for i in indexes_non_traversable:
            self._cells[i].is_traversable = False

    def cells(self) -> list[Traversable]:
        return self._cells

    def num_cells_all(self) -> int:
        return len(self.cells())


class TestContainerTraversable:

    @pytest.fixture(scope="class", autouse=True)
    def setup_class(self, request):
        request.cls.c_full = Container()
        request.cls.c_empty = Container([0, 1, 2, 3])
        request.cls.c_med = Container([2])

    def test_cells_traversable(self):
        assert len(self.c_full.cells_traversable()) == 4
        assert len(self.c_empty.cells_traversable()) == 0
        assert len(self.c_med.cells_traversable()) == 3
        
    def test_num_cells_traversable(self):
        assert self.c_full.num_cells_traversable() == 4
        assert self.c_empty.num_cells_traversable() == 0
        assert self.c_med.num_cells_traversable() == 3
        
    def test_num_cells_non_traversable(self):
        assert self.c_full.num_cells_non_traversable() == 0
        assert self.c_empty.num_cells_non_traversable() == 4
        assert self.c_med.num_cells_non_traversable() == 1
        
    def test_pct_cells_traversable(self):
        assert self.c_full.pct_cells_traversable() == 1
        assert self.c_empty.pct_cells_traversable() == 0
        assert self.c_med.pct_cells_traversable() == 0.75
        
    def test_pct_cells_non_traversable(self):
        assert self.c_full.pct_cells_non_traversable() == 0
        assert self.c_empty.pct_cells_non_traversable() == 1
        assert self.c_med.pct_cells_non_traversable() == 0.25
        