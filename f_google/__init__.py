from f_core.imports import ULazy

ULazy.install(globals(), {
    'Auth': 'f_google.creds.auth:Auth',
    'OAuth': 'f_google.creds.oauth:OAuth',
    'BigQuery': 'f_google.services.bigquery:BigQuery',
    'Drive': 'f_google.services.drive:Drive',
    'Gemini': 'f_google.services.gemini:Gemini',
    'Spread': 'f_google.services.sheets:Spread',
})
