from f_hs.algo.i_0_base._search_state import SearchStateSPP
from f_hs.algo.i_0_base.main import AlgoSPP
from f_hs.frontier.i_1_fifo.main import FrontierFIFO
from f_hs.problem.i_0_base.main import ProblemSPP
from f_hs.state.i_0_base.main import StateBase
from typing import Generic, TypeVar

State = TypeVar('State', bound=StateBase)


class BFS(Generic[State], AlgoSPP[State]):
    """
    ========================================================================
     Breadth-First Search Algorithm.
    ========================================================================
    """

    # Factory
    Factory: type = None

    def __init__(self,
                 problem: ProblemSPP[State],
                 name: str = 'BFS',
                 is_recording: bool = False,
                 search_state: SearchStateSPP[State] | None = None
                 ) -> None:
        """
        ====================================================================
         Init private Attributes. See AlgoSPP for `search_state`.
        ====================================================================
        """
        AlgoSPP.__init__(self,
                         problem=problem,
                         frontier=FrontierFIFO[State](),
                         name=name,
                         is_recording=is_recording,
                         search_state=search_state)
