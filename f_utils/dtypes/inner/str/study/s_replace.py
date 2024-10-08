from f_utils.dtypes.u_str import UStr


s = 'I go to Toronto'
d = {'to': 'tx'}

print(UStr.replace.by_dict(s=s, d=d))
print(UStr.replace.by_dict_with_spaces(s=s, d=d))
print(UStr.replace.by_dict_with_spaces(s='I want to', d=d))