from study.mixin.mixin_even import MixinEven


class Grid(MixinEven):

    def __init__(self):
        MixinEven.__init__(self, func_elements='cells')

    def cells(self) -> list[int]:
        return list(range(10))



grid = Grid()
print(grid.cells_even())

