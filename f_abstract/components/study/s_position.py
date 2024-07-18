from f_abstract.components.position import Position


pos = Position()
pos.relative = (50, 50, 50, 50)
pos.update(200, 300)
print(pos)