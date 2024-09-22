from f_google.big_query.structures.schema import Schema
from proj.noteret.tiktok.fields import Fields


class Schemas:
    """
    ============================================================================
     Class of Schemas for Noteret-Tiktok project.
    ============================================================================
    """

    @staticmethod
    def user() -> Schema:
        """
        ========================================================================
         Return Schema with User info.
        ========================================================================
        """
        schema = Schema()
        schema.add(Fields.ID_USER)
        schema.add(Fields.NICK)
        schema.add(Fields.REGION)
        schema.add(Fields.SECRET)
        schema.add(Fields.VERIFIED)
        schema.add(Fields.AWEME)
        schema.add(Fields.FAVORITED)
        schema.add(Fields.FOLLOWERS)
        schema.add(Fields.FOLLOWING)
        return schema
