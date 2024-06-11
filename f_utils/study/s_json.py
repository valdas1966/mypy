from f_utils import u_json


def study_file():
    path = 'g:\\jsons\\myq.json'
    data = u_json.file_to_dict(path=path)
    print(data)


def study_str():
    s = '{k_1=v_1, k_2=v_2}'
    d = u_json.to_dict(str_json=s)
    print(d)


study_str()

