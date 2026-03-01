from f_google.auth.main import Auth
from f_google.auth._enums import ServiceAccount
from f_google.auth._factory import Factory
from google.oauth2.service_account import Credentials

Auth.Factory = Factory
