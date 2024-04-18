from f_heuristic_search.problem_types.mixin.has_goals import (HasGoals,
                                                              NodePath as Node)


def test_active_goals():
    goal_a = Node(name='A')
    goal_b = Node(name='B')
    goals = (goal_a, goal_b)
    kspp = HasGoals(goals=goals)
    assert kspp.goals_active == set(goals)
    kspp.remove_goal_active(goal=goal_a)
    assert kspp.goals_active == {goal_b}
