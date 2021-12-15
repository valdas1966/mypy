
class Canvas:

    def __init__(self, coor=None):
        self.left = 0
        self.top = 0
        self.width = 100
        self.height = 100
        if coor:
            assert type(coor) == tuple
            assert len(coor) == 4
            self.left, self.top, self.width, self.height = coor

    def get_coor(self, ratios):
        left = self.left + self.ratio(ratios[0], self.width)
        top = self.top + self.ratio(ratios[1], self.height)
        width = self.ratio(ratios[2], self.width)
        height = self.ratio(ratios[3], self.height)
        return left, top, width, height

    @classmethod
    def ratio(cls, part, whole):
        return whole / 100 * part
