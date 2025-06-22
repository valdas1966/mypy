from .client import Client
from ._internal.factory import FactoryClientHttp

Client.Factory = FactoryClientHttp
