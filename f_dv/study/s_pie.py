from f_dv.pie import Pie


labels = ['Alive', 'Dead']
pcts = [90, 10]
name = 'Distribution of Alive/Dead People'

Pie(name=name, labels=labels, pcts=pcts).show()
