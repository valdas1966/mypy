from f_proj.rapid_api.data.i_0_audit import DataAudit
from f_proj.rapid_api.data.i_0_list import DataList, Flattenable
from pydantic import Field
from typing import ClassVar


class Challenge(DataAudit):
    """
    ============================================================================
     Challenge.
    ============================================================================
    """
    id: int = Field(default=None)
    name: str = Field(default=None)


class ChallengeList(DataList[Challenge]):
    has_more: bool = Field(default=None)
    cursor: int = Field(default=None)
    rows_key: ClassVar[str] = "challenge_list"


class DataResponse(DataAudit):
    data: ChallengeList = Field(default=None, alias='data')


response = {
            'data': {
                        'has_more': True,
                        'cursor': 10,
                        'challenge_list':
                        [
                            {'id': '1', 'name': 'AAA'},
                            {'id': '2', 'name': 'BBB'}
                        ]
                     }
            }

data = DataResponse.model_validate(response)
print(data)


