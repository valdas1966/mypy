
ops = ['A', 'B']
input = None

for op in ops:
    op(input) if op is 'Inputtable' else op()
    if not a.is_valid:
        break
    if a is 'Outtable':
        output = a.output()
    if a is 'Resulttable':
        out = a.out()
        b = ops[i+1]()
