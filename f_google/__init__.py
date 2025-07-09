from ._factory import Google, Factory
from ._internal.auth import Auth, Credentials, ServiceAccount
from ._internal.services.storage import Storage

Google.Factory = Factory
