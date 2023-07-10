from f_utils import u_random


values = [1, 2, 3]

groups = u_random.to_groups(values, n=7, k=2)

print(sorted(groups))
