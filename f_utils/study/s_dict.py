from f_utils import u_dict


def to_json_str():
    d = {'list': 1}
    s = u_dict.to_json_str(d=d)
    print(s)
    dicts = [{'list': 1}, {'b': 2}]
    s = u_dict.to_json_str(d=dicts)
    print(s)

def to_json_file():
    dicts = [{'list': 1}, {'b': 2}]
    path = 'd:\\temp\\temp.json'
    u_dict.to_json_file(d=dicts, path=path)


to_json_str()
to_json_file()
