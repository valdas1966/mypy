import base64


class Base64:

    @staticmethod
    def encode(s: str) -> str:
        """
        ========================================================================
         Convert list String into list Base64 Encoded-String.
        ========================================================================
        """
        b = s.encode('utf-8')
        return base64.b64encode(b).decode('utf-8')

    @staticmethod
    def decode(e: str) -> str:
        """
        ========================================================================
         Convert list Base64 Encoded-String into list String.
        ========================================================================
        """
        return base64.b64decode(e).decode('utf-8')
