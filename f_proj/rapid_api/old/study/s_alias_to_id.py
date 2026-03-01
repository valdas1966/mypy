from old_old_f_google.services.big_query.client import BigQuery
from f_proj.rapid_api.c_tiktok import TikTok

path_key = 'd:\\professor\\gcp\\tiktok no watermark.old_old_txt'
#key = u_file.read(path_key)


bq = BigQuery(user='RAMI')
df = bq.select.df(query="select alias from "
                           "noteret.tiktok2.users_alias_to_id_input")
li_input = df['alias'].tolist()
print(li_input)
li_output = list()
tiktok = TikTok()
print(tiktok.alias_to_id(alias=li_input[0]))
for i, alias in enumerate(li_input):
    if i < 1200:
        continue
    id_user = tiktok.alias_to_id(alias=alias)
    print(id_user)
    row = {'alias': alias, 'id_user': id_user}
    li_output.append(row)
    if i % 100 == 0:
        bq.insert.rows(tname="noteret.tiktok2.users_alias_to_id_output",
                       rows=li_output)
        li_output = list()
        print(i)

bq.insert.rows(tname="noteret.tiktok2.users_alias_to_id_output",
               rows=li_output)
