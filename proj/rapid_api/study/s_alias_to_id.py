from f_google.big_query.client import BigQuery
from proj.rapid_api.c_tiktok import TikTok
from f_utils import u_file


path_key = 'd:\\professor\\gcp\\tiktok no watermark.old_old_txt'
key = u_file.read(path_key)


bq = BigQuery(user='RAMI')
df = bq.select.to_df(query="select alias from "
                           "noteret.tiktok2.users_alias_to_id_input")
li_input = df['alias'].tolist()
li_output = list()
tiktok = TikTok(key=key)
for i, alias in enumerate(li_input):
    if i < 1200:
        continue
    id_user = tiktok.alias_to_id(alias=alias)
    row = {'alias': alias, 'id_user': id_user}
    li_output.append(row)
    if i % 100 == 0:
        bq.insert.rows(tname="noteret.tiktok2.users_alias_to_id_output",
                       rows=li_output)
        li_output = list()
        print(i)

bq.insert.rows(tname="noteret.tiktok2.users_alias_to_id_output",
               rows=li_output)