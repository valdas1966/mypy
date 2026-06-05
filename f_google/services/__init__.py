from typing import TYPE_CHECKING

from f_core.imports import ULazy

if TYPE_CHECKING:
    from f_google.services.bigquery import BigQuery
    from f_google.services.drive import Drive
    from f_google.services.gemini import Gemini
    from f_google.services.sheets import Spread

ULazy.install(globals(), {
    'BigQuery': 'f_google.services.bigquery:BigQuery',
    'Drive': 'f_google.services.drive:Drive',
    'Gemini': 'f_google.services.gemini:Gemini',
    'Spread': 'f_google.services.sheets:Spread',
})
