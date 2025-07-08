from .main import Storage
from ._factory import Factory
from f_google._internal.auth import Auth, ServiceAccount


def test_storage_connection() -> None:
    """
    ========================================================================
    Test basic storage connection and bucket listing.
    ========================================================================
    """
    storage = Factory.rami()
    buckets = storage.list_buckets()
    assert isinstance(buckets, list)
    print(f"Connected successfully. Found {len(buckets)} buckets.")


def test_bucket_access() -> None:
    """
    ========================================================================
    Test bucket access using __getitem__ method.
    ========================================================================
    """
    storage = Factory.rami()
    buckets = storage.list_buckets()
    if buckets:
        bucket_name = buckets[0]
        bucket = storage[bucket_name]
        assert bucket.name == bucket_name
        print(f"Bucket access test passed for: {bucket_name}")
    else:
        print("No buckets available for testing")


def test_bucket_creation_deletion() -> None:
    """
    ========================================================================
    Test bucket creation and deletion operations.
    WARNING: This test creates and deletes a bucket.
    ========================================================================
    """
    storage = Factory.rami()
    test_bucket_name = "test-bucket-12345"
    
    try:
        # Test bucket creation
        bucket = storage.create_bucket(test_bucket_name)
        assert bucket.name == test_bucket_name
        print(f"Bucket created successfully: {test_bucket_name}")
        
        # Verify bucket exists in listing
        buckets = storage.list_buckets()
        assert test_bucket_name in buckets
        
    finally:
        # Clean up - delete test bucket
        try:
            storage.delete_bucket(test_bucket_name)
            print(f"Bucket deleted successfully: {test_bucket_name}")
        except Exception as e:
            print(f"Error deleting test bucket: {e}")


def test_storage_factory_patterns() -> None:
    """
    ========================================================================
    Test storage factory pattern methods for different service accounts.
    ========================================================================
    """
    # Test RAMI storage
    storage_rami = Factory.rami()
    buckets_rami = storage_rami.list_buckets()
    print(f"RAMI storage: {len(buckets_rami)} buckets")
    
    # Test VALDAS storage
    storage_valdas = Factory.valdas()
    buckets_valdas = storage_valdas.list_buckets()
    print(f"VALDAS storage: {len(buckets_valdas)} buckets")
    
    # Test generic factory method
    storage_generic = Factory.from_account(ServiceAccount.RAMI)
    buckets_generic = storage_generic.list_buckets()
    assert buckets_rami == buckets_generic
    print("Storage factory pattern tests passed")


def test_bucket_wrapper_integration() -> None:
    """
    ========================================================================
    Test integration between storage and bucket wrapper classes.
    ========================================================================
    """
    storage = Factory.rami()
    buckets = storage.list_buckets()
    
    if buckets:
        bucket_name = buckets[0]
        
        # Test get_bucket method
        bucket1 = storage.get_bucket(bucket_name)
        assert bucket1.name == bucket_name
        
        # Test __getitem__ method
        bucket2 = storage[bucket_name]
        assert bucket2.name == bucket_name
        
        # Both should be equivalent
        assert bucket1.name == bucket2.name
        print(f"Bucket wrapper integration test passed for: {bucket_name}")
    else:
        print("No buckets available for integration testing")


def run_all_tests() -> None:
    """
    ========================================================================
    Run all storage-level tests in sequence.
    ========================================================================
    """
    print("Running Google Cloud Storage (storage-level) tests...")
    
    try:
        test_storage_connection()
        test_bucket_access()
        test_storage_factory_patterns()
        test_bucket_wrapper_integration()
        
        # Uncomment this test if you want to test bucket creation/deletion
        # WARNING: This test creates and deletes buckets
        # test_bucket_creation_deletion()
        
        print("All storage-level tests completed successfully!")
        
    except Exception as e:
        print(f"Storage test failed: {e}")
        raise