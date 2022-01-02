
class Canvas:

    def __init__(self, coor=None):
        self.left = 0
        self.top = 0
        self.width = 1
        self.height = 1
        if coor:
            assert type(coor) == tuple
            assert len(coor) == 4
            self.left, self.top, self.width, self.height = coor

    def get_coor(self, ratios):
        left = self.left + (ratios[0] * self.width)
        top = self.top + (ratios[1] * self.height)
        width = ratios[2] * self.width
        height = ratios[3] * self.height
        return left, top, width, height
