import os


class User:
    """
    ============================================================================
     Enum for Google-User.
    ============================================================================
    """

    VALDAS = str(os.getenv(key='VALDAS_JSON_PATH'))
    # Try get RAMI_JSON_PATH from environment variable
    #  on fail, use default path
    try:
        RAMI = str(os.getenv(key='RAMI_JSON_PATH'))
    except:
        RAMI = 'd:\\professor\\JSON\\viewer.json'
    GFUNC = 'd:\\professor\\json\\gfunc.json'
