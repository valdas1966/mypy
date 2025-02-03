from collections import Counter


c = Counter()
c['a'] += 1
c['a'] += 1
c['b'] += 1

print(c['a'])
print(c['b'])
