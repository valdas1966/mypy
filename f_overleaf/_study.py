from f_overleaf import OverLeaf


overleaf = OverLeaf.Factory.valdas()
for project in overleaf.values():
    print(project)
