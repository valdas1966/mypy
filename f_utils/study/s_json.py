from f_utils import u_json


path = 'g:\\jsons\\myq.json'

data = u_json.file_to_dict(path=path)

print(data)
