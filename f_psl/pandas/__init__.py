from f_core.imports import ULazy

ULazy.install(globals(), {
    'UDf': 'f_psl.pandas.df:UDf',
    'UCsv': 'f_psl.pandas.csv:UCsv',
})
