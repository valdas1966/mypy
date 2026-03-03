from f_google.auth.main import Auth
from f_google.auth._enums import Account, TypeAuth
from f_google.auth._factory import Factory
from google.auth.credentials import Credentials

Auth.Factory = Factory
