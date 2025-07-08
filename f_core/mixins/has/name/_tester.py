from f_core.mixins.has.name.main import HasName


def test_has_name():
    """
    ============================================================================
     Test HasName mixin functionality.
    ============================================================================
    """
    # Test with name
    name_obj = HasName("test_name")
    assert name_obj.name == "test_name"
    assert name_obj.key_comparison() == ["test_name"]
    assert str(name_obj) == "test_name"
    assert hash(name_obj) == hash("test_name")
    
    # Test with None name
    none_name_obj = HasName()
    assert none_name_obj.name is None
    assert none_name_obj.key_comparison() == [""]
    assert str(none_name_obj) == "None"
    assert hash(none_name_obj) == hash(None)
    
    # Test with empty string
    empty_name_obj = HasName("")
    assert empty_name_obj.name == ""
    assert empty_name_obj.key_comparison() == [""]
    assert str(empty_name_obj) == ""
    assert hash(empty_name_obj) == hash("")
    
    print("HasName tests passed!")


if __name__ == "__main__":
    test_has_name()