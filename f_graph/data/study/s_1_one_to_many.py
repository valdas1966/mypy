from f_graph.data.i_2_one_to_many import DataOneToMany, NodePath
from f_graph.problems.u_2_one_to_many import ProblemOneToMany, UProblemOneToMany
from f_ds.queues.i_1_fifo import QueueFIFO


p = UProblemOneToMany.gen_3x3()
goal_1, goal_2 = p.goals
print('Problem Goals:')
print('--------------')
print(goal_1)
print(goal_2)
data = DataOneToMany(problem=p, type_queue=QueueFIFO)
print('Active Goals:')
print('---------------')
print(data.goals_active)
data.goals_active.remove(goal_1)
print('Active Goals:')
print('---------------')
print(data.goals_active)