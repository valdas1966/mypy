from f_hs.solution.main import (
    SolutionSPP,
    SolutionOMSPP,
    SolutionMOSPP,
)
from f_hs.solution.per_key import SolutionPerKey
from f_hs.solution._factory import Factory

SolutionSPP.Factory = Factory
