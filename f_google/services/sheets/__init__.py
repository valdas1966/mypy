from f_core.imports import ULazy

ULazy.install(globals(), {
    'Spread': 'f_google.services.sheets.spread:Spread',
    'Sheet': 'f_google.services.sheets.sheet:Sheet',
    'Cell': 'f_google.services.sheets.cell:Cell',
})
