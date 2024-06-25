import string


class Base52:
    """
    ============================================================================
     Base-52 (only letters) Encoder.
    ============================================================================
    """

    # Define the custom alphabet with only letters
    _CHARS = string.ascii_letters  # 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ'
    _BASE = len(_CHARS)

    @staticmethod
    def encode(s: str) -> str:
        """
        ========================================================================
         Encode a String into a custom Base52 Encoded-String.
        ========================================================================
        """
        b = s.encode('utf-8')
        num = int.from_bytes(b, 'big')
        if num == 0:
            return Base52._CHARS[0]
        e = list()
        while num:
            num, rem = divmod(num, Base52._BASE)
            e.append(Base52._CHARS[rem])
        return ''.join(reversed(e))

    @staticmethod
    def decode(e: str) -> str:
        """
        ========================================================================
         Decode a custom Base52 Encoded-String back to the original String.
        ========================================================================
        """
        num = 0
        for char in e:
            if char not in Base52._CHARS:
                raise ValueError(f"Invalid character found: {char}")
            num = num * Base52._BASE + Base52._CHARS.index(char)
        # Convert number back to bytes
        len_byte = (num.bit_length() + 7) // 8
        d = num.to_bytes(len_byte, 'big')
        return d.decode('utf-8')
