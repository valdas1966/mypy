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
        schema.append(Fields.ID_USER)
        schema.append(Fields.NICK)
        schema.append(Fields.REGION)
        schema.append(Fields.SECRET)
        schema.append(Fields.VERIFIED)
        schema.append(Fields.AWEME)
        schema.append(Fields.FAVORITED)
        schema.append(Fields.FOLLOWERS)
        schema.append(Fields.FOLLOWING)
        schema.append(Fields.INSERTED)
        return schema

    @staticmethod
    def followers() -> Schema:
        schema = Schemas.user()
        schema.insert(1,Fields.ID_FOLLOWER)
        return schema

