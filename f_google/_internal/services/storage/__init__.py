from .main import Storage
from .bucket import Bucket
from .blob import Blob
from .folder import Folder
from .file import File
from ._factory import Factory

# Set up factory pattern integration
Storage.Factory = Factory