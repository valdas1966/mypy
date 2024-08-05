import re


s = "some_string{list{b,c}}some_string"
match = re.search(r"{[^{}]*{[^{}]*}}", s)
print(match.group(0))
