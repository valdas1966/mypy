from f_graph.data.i_1_one_to_many import DataOneToMany
from f_graph.problems.u_2_one_to_many import UProblemOneToMany as u_problem
from f_ds.queues.i_1_fifo import QueueFIFO


def test_goals_active():
    problem = u_problem.gen_3x3()
    data = DataOneToMany(problem=problem, type_queue=QueueFIFO)
    assert problem.goals == data.goals_active
    data.goals_active.pop()
    assert len(data.goals_active) == 1
