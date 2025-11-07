from f_ds.grids.cell.i_1_map.main import CellMap


zero = CellMap.Factory.zero()
one = CellMap.Factory.one()

print(hash(zero))
print(hash(one))
