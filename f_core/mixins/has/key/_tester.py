from f_core.mixins.has.key.main import HasKey


def test_has_key():
    """
    ============================================================================
     Test HasKey mixin functionality.
    ============================================================================
    """
    # Test basic functionality
    key_obj = HasKey("test_key")
    assert key_obj.key == "test_key"
    assert key_obj.key_comparison() == "test_key"
    assert hash(key_obj) == hash("test_key")
    
    # Test with different key types
    int_key_obj = HasKey(42)
    assert int_key_obj.key == 42
    assert hash(int_key_obj) == hash(42)
    
    print("HasKey tests passed!")


if __name__ == "__main__":
    test_has_key()