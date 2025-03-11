from f_proj.rapid_api.data.i_0_audit import DataAudit
from f_proj.rapid_api.data.i_2_user import DataUser
from pydantic import Field


class DataUsersById(DataAudit):
    """
    ============================================================================
     Data-Class for request 'Users by ID'.
    ============================================================================
    """
    user: DataUser = Field(default=None, alias='data')

    def fill(self, **kwargs) -> None:
        """
        ============================================================================
         Fill the data-class with the given kwargs.
        ============================================================================
        """
        filled = self.model_validate(kwargs)
        self.__dict__.update(filled.__dict__)

    class Config:
        """
        ============================================================================
         Config for request 'Users by ID'.
        ============================================================================
        """
        populate_by_name = True
        extra = 'allow'  # allows setting arbitrary attributes like 'is_ok'
