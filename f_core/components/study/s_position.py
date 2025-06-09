from f_gui.geometry.geometry import Position


pos = Position()
pos.relative = (50, 50, 50, 50)
pos.update(200, 300)
print(pos)