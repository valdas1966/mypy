from f_google.big_query.structures.schema import Schema
from proj.noteret.tiktok.fields import Fields


class Schemas:
    """
    ============================================================================
     Class of Schemas for Noteret-Tiktok project.
    ============================================================================
    """

    @staticmethod
    def user_info() -> Schema:
        """
        ========================================================================
         Return Schema with User info.
        ========================================================================
        """
        schema = Schema()
        schema.append(Fields.ID_USER)
        schema.append(Fields.NICK)
        schema.append(Fields.REGION)
        schema.append(Fields.IS_SECRET)
        schema.append(Fields.IS_VERIFIED)
        schema.append(Fields.IS_PRIVATE)
        return schema

    @staticmethod
    def user_stats() -> Schema:
        """
        ========================================================================
         Return Schema with User's Stats.
        ========================================================================
        """
        schema = Schema()
        schema.append(Fields.AWEME)
        schema.append(Fields.FAVORITED)
        schema.append(Fields.VIDEOS)
        schema.append(Fields.HEARTS)
        schema.append(Fields.DIGGS)
        schema.append(Fields.FOLLOWERS)
        schema.append(Fields.FOLLOWING)
        return schema

    @staticmethod
    def audit() -> Schema:
        """
        ========================================================================
         Return Schema with Audit columns.
        ========================================================================
        """
        schema = Schema()
        schema.append(Fields.INSERTED)
        return schema

    @staticmethod
    def users() -> Schema:
        schema = Schemas.user_info() + Schemas.user_stats()
        schema.append(Fields.INSERTED)
        return schema

    @staticmethod
    def users_snapshots() -> Schema:
        schema = Schemas.users()
        schema.insert(-2, Fields.SOURCE)
        return schema

    @staticmethod
    def followers() -> Schema:
        schema = Schema()
        schema.append(Fields.ID_USER)
        schema.append(Fields.ID_FOLLOWER)
        schema.append(Fields.INSERTED)
        return schema
