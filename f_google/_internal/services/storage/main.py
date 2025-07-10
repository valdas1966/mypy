from google.cloud import storage
from f_core.mixins.validatable import Validatable
from f_google.google import Credentials


class Storage(Validatable):
    """
    ============================================================================
     Google Cloud Storage client wrapper with enhanced functionality.
    ============================================================================
    """

    # Factory
    Factory: type = None

    def __init__(self, creds: Credentials) -> None:
        """
        ========================================================================
         Initialize Storage client with credentials.
        ========================================================================
        """
        self._client = storage.Client(credentials=creds)
        Validatable.__init__(self, is_valid=bool(self._client))

    def names_buckets(self) -> list[str]:
        """
        ========================================================================
         Get names of all buckets in the storage.
        ========================================================================
        """
        return [bucket.name for bucket in self._client.list_buckets()]  
    
    def is_exist_bucket(self, name_bucket: str) -> bool:
        """
        ========================================================================
         Check if a bucket exists in the storage.
        ========================================================================
        """
        return name_bucket in self.names_buckets()
    
    def is_exist_file(self, name_bucket: str, path_dst: str) -> bool:
        """
        ========================================================================
         Check if a file exists in the storage.
        ========================================================================
        """
        return self.is_exist_bucket(name_bucket) and self._client.bucket(name_bucket).blob(path_dst).exists()   
    
    def upload_file(self,
                    # Name of the Bucket where the file will be uploaded.
                    name_bucket: str,
                    # Path of the file to be uploaded.
                    path_src: str,
                    # Path of the file in the Bucket 
                    path_dst: str) -> None:
        """
        ========================================================================
         Upload a file to the storage.
        ========================================================================
        """
        bucket = self._client.bucket(name_bucket)
        blob = bucket.blob(path_dst)
        blob.upload_from_filename(path_src)


    