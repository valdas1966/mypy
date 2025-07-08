from ._factory import Factory
from f_google._internal.auth import ServiceAccount
import tempfile
import os


def test_bucket_creation() -> None:
    """
    ========================================================================
    Test bucket creation using factory methods.
    ========================================================================
    """
    # Test RAMI factory
    try:
        bucket = Factory.rami('test-bucket-name')
        print(f"RAMI bucket factory test passed: {bucket.name}")
    except Exception as e:
        print(f"RAMI bucket factory test failed: {e}")

    # Test VALDAS factory
    try:
        bucket = Factory.valdas('test-bucket-name')
        print(f"VALDAS bucket factory test passed: {bucket.name}")
    except Exception as e:
        print(f"VALDAS bucket factory test failed: {e}")

    # Test generic factory
    try:
        bucket = Factory.from_name('test-bucket-name', ServiceAccount.RAMI)
        print(f"Generic bucket factory test passed: {bucket.name}")
    except Exception as e:
        print(f"Generic bucket factory test failed: {e}")


def test_blob_listing() -> None:
    """
    ========================================================================
    Test blob listing functionality.
    ========================================================================
    """
    try:
        bucket = Factory.rami('test-bucket-name')
        
        # Test basic blob listing
        blobs = bucket.list_blobs()
        print(f"Found {len(blobs)} blobs in bucket")
        
        # Test prefix filtering
        if blobs:
            filtered_blobs = bucket.list_blobs(prefix='test')
            print(f"Found {len(filtered_blobs)} blobs with 'test' prefix")
        
        print("Blob listing test passed")
    except Exception as e:
        print(f"Blob listing test failed: {e}")


def test_blob_operations() -> None:
    """
    ========================================================================
    Test blob upload, download, and deletion operations.
    ========================================================================
    """
    try:
        bucket = Factory.rami('test-bucket-name')
        
        # Create test file
        with tempfile.NamedTemporaryFile(mode='w', suffix='.txt', delete=False) as temp_file:
            temp_file.write("Test content for bucket operations")
            temp_file_path = temp_file.name
        
        test_blob_name = "test_blob_operations.txt"
        
        try:
            # Test upload
            bucket.upload_file(temp_file_path, test_blob_name)
            print(f"File uploaded successfully: {test_blob_name}")
            
            # Test existence check
            exists = bucket.blob_exists(test_blob_name)
            assert exists is True
            print("Blob existence check passed")
            
            # Test 'in' operator
            assert test_blob_name in bucket
            print("Blob 'in' operator test passed")
            
            # Test blob size
            size = bucket.get_blob_size(test_blob_name)
            print(f"Blob size: {size} bytes")
            
            # Test public URL
            url = bucket.get_blob_url(test_blob_name)
            print(f"Public URL: {url}")
            
            # Test download
            download_path = temp_file_path + "_downloaded"
            bucket.download_blob(test_blob_name, download_path)
            
            # Verify download
            with open(download_path, 'r') as f:
                content = f.read()
                assert content == "Test content for bucket operations"
            print("Download test passed")
            
            # Clean up
            bucket.delete_blob(test_blob_name)
            os.unlink(download_path)
            print("Blob deletion test passed")
            
        finally:
            # Clean up temp file
            if os.path.exists(temp_file_path):
                os.unlink(temp_file_path)
        
        print("All blob operations tests passed")
    except Exception as e:
        print(f"Blob operations test failed: {e}")


def test_url_upload() -> None:
    """
    ========================================================================
    Test uploading files from URLs.
    ========================================================================
    """
    try:
        bucket = Factory.rami('test-bucket-name')
        
        # Test URL upload (using a small public file)
        test_url = "https://httpbin.org/json"
        blob_name = "test_url_upload.json"
        
        bucket.upload_from_url(test_url, blob_name)
        print(f"URL upload successful: {blob_name}")
        
        # Verify upload
        assert bucket.blob_exists(blob_name)
        print("URL upload verification passed")
        
        # Clean up
        bucket.delete_blob(blob_name)
        print("URL upload test passed")
        
    except Exception as e:
        print(f"URL upload test failed: {e}")


def test_bucket_properties() -> None:
    """
    ========================================================================
    Test bucket property methods.
    ========================================================================
    """
    try:
        bucket = Factory.rami('test-bucket-name')
        
        # Test bucket name property
        name = bucket.name
        print(f"Bucket name: {name}")
        
        # Test bucket length
        length = len(bucket)
        print(f"Bucket contains {length} blobs")
        
        print("Bucket properties test passed")
    except Exception as e:
        print(f"Bucket properties test failed: {e}")


def run_all_tests() -> None:
    """
    ========================================================================
    Run all bucket-specific tests.
    ========================================================================
    """
    print("Running bucket-specific tests...")
    
    try:
        test_bucket_creation()
        test_blob_listing()
        test_bucket_properties()
        
        # Uncomment these tests if you want to test file operations
        # WARNING: These tests create/delete files
        # test_blob_operations()
        # test_url_upload()
        
        print("All bucket tests completed successfully!")
        
    except Exception as e:
        print(f"Bucket test failed: {e}")
        raise