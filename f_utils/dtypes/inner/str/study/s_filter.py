from f_utils.dtypes.inner.str.filter import Filter


word = '(Spartak)'
chars = {'(', ')'}

print(Filter.specific_chars(s=word, chars=chars))
