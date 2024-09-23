from f_google.big_query.client import BigQuery
from proj.noteret.tiktok.schemas import Schemas


pre = 'noteret.tiktok'


def followers() -> None:
    tname = f'{pre}.followers'
    schema = Schemas.followers()
    bq = BigQuery()
    bq.create.table(tname=tname, schema=schema)


followers()
