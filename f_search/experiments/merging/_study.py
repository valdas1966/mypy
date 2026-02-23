from f_utils import u_pickle


path_problems = 'f:\\paper\\i_3_problems\\100k\\problems.pkl'
path_solutions = 'f:\\paper\\i_4_solutions\\dijkstra.pkl'


item = u_pickle.load(path=path_problems)
print(type(item))
