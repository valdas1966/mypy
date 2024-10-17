from f_graph.termination.one_to_one.i_0_goal import TerminationGoal, NodePath

goal = NodePath(name='GOAL')


def test_goal():
    t = TerminationGoal(goal=goal)
    assert t.can(node=goal)
    