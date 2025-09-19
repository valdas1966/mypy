from f_utils import u_pickle


generated = u_pickle.load(path='g:\\temp\\generated.pkl')
generated.update()
print(type(generated))

best = generated.pop()
next = generated.pop()
print(best < next)
