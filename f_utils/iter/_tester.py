from f_utils.iter._factory import Factory
from f_utils.iter import u_iter


def test_sample() -> None:
    """
    ========================================================================
     Test the sample function.
    ========================================================================
    """
    data = Factory.ab()
    pct = 50
    sample = u_iter.sample(data=data, pct=pct)
    assert len(sample) == 1
