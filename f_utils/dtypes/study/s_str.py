from f_utils.dtypes.u_str import UStr


s = 'abcdef'
li = UStr.split.by_length(s=s, length=3)
print(li)