from f_gui.components.position import Position


pos = Position()
pos.relative = (50, 50, 50, 50)
pos.update(200, 300)
print(pos)