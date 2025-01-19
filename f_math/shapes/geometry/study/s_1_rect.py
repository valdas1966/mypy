from f_math.shapes.geometry.i_1_rect import GeometryRect, DataGeoRect


geo_win = DataGeoRect(top=10, left=10, width=80, height=80)
win = GeometryRect(data_geo=geo_win, is_relative=False)
print(f'win.absolute: {win.absolute}')

geo_rect = DataGeoRect(top=10, left=10, width=80, height=80)
rect = GeometryRect(data_geo=geo_rect, is_relative=True)
print(f'rect.relative: {rect.relative}')


rect.update(geo_parent=win.absolute)
print(f'rect.absolute after update: {rect.absolute}')
