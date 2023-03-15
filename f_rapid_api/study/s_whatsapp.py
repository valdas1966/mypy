from f_rapid_api.c_whatsapp import WhatsApp
from f_utils import u_file


json_key = path_key = 'd:\\professor\\gcp\\owner.json'
path_key = 'd:\\professor\\gcp\\whatsapp profile pic.txt'

key = u_file.read(path_key)
tel = '972562000072'
folder = 'd:\\temp\\2023\\02'


w = WhatsApp(key=key)
w.tel_to_pic(tel=tel, folder=folder)

