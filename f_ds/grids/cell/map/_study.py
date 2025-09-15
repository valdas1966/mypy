from f_ds.grids.cell.map.main import CellMap


zero = CellMap.Factory.zero()
one = CellMap.Factory.one()

print(hash(zero))
print(hash(one))
