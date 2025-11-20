from f_search.stats.i_2_omspp.main import StatsOMSPP, State


def test_ab():
    """
    ========================================================================
     Test the StatsOMSPP.Factory.ab() method.
    ========================================================================
    """
    stats = StatsOMSPP.Factory.ab()
    assert stats.elapsed == 30
    assert stats.generated == 30
    assert stats.updated == 30
    assert stats.explored == 30
    state_a = State.Factory.a()
    assert stats[state_a].elapsed == 10
    assert stats[state_a].generated == 10
    assert stats[state_a].updated == 10
    assert stats[state_a].explored == 10
    state_b = State.Factory.b()
    assert stats[state_b].elapsed == 20
    assert stats[state_b].generated == 20
    assert stats[state_b].updated == 20
    assert stats[state_b].explored == 20
