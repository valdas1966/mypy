from f_rapid_api.c_tiktok import TikTok
from f_db.c_bq import BigQuery
from f_utils import u_file
import time


path_rapid = 'd:\\professor\\gcp\\tiktok no watermark.old_old_txt'
key_rapid = u_file.read(path_rapid)
tiktok = TikTok(key=key_rapid)

path_gcp = 'd:\\tiktok2\\repo\\viewer.json'
bq = BigQuery(json_key=path_gcp)
tname = 'noteret.tiktok2.users_alias_to_id'
tname_input = tname + '_input'
tname_output = tname + '_output'
aliases = bq.select_list(query='select alias from ' + tname_input)
d = {alias: tiktok.alias_to_id(alias)
     for alias
     in aliases}
rows = [{'alias': alias, 'id_user': id_user}
        for alias, id_user
        in d.items()]
bq.run(command='truncate table ' + tname_output)
is_ready = False
for i in range(30):
    if is_ready:
        break
    time.sleep(10)
    try:
        bq.insert_rows(tname=tname_output, rows=rows)
        is_ready = True
    except Exception as e:
        pass
print(bq.select(query=tname_output))
bq.close()
