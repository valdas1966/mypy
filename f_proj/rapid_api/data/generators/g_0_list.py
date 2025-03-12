from f_proj.rapid_api.data.i_0_list import DataList, Flattenable
from pydantic import Field
from typing import ClassVar


class Challenge(Flattenable):
    """
    ============================================================================
     Challenge.
    ============================================================================
    """
    id: int = Field(default=None)
    name: str = Field(default=None)


class ChallengeList(DataList[Challenge]):
    rows_key: ClassVar[str] = "challenge_list"



response = {
    'has_more': True,
    'cursor': 10,
    'challenge_list': [
        {'id': '1', 'name': 'AAA'},
        {'id': '2', 'name': 'BBB'}
    ]
}

data = ChallengeList.model_validate(response)
print(data)


