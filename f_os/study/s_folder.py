from f_os import u_folder


folder = 'd:\\mypy\\f_os'

filepaths = u_folder.filepaths(folder=folder)

for f in filepaths:
    print(f)

print()

paths_rel = u_folder.filepaths_without_common(paths=filepaths)

for f in paths_rel:
    print(f)
