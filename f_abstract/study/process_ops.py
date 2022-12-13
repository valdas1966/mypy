
ops = list()
ops.append({'class': 'A', 'input': 'name'})
ops.append({'class': 'B', 'input': 'family'})

start = None
input = None
for i, op in enumerate(ops):
    if i == 0:
        if start_name:
            res = op['class'](start_name=start_value)
        else:
            res = op['class']()
    else:

    if op['input']:
        input =
    res = op()
    res = op['class']()
    if not res['is_valid']:
        break
    input = res['']
    op(input) if op is 'Inputtable' else op()
    if not a.is_valid:
        break
    if a is 'Outtable':
        output = a.output()
    if a is 'Resulttable':
        out = a.out()
        b = ops[i+1]()
