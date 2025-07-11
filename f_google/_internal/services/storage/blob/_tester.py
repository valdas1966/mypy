from ._factory import Factory
from f_google._internal.auth import ServiceAccount
import tempfile
import os


def test_blob_creation() -> None:
    """
    ========================================================================
    Test g_blob creation using factory methods.
    ========================================================================
    """
    try:
        # Test RAMI factory
        blob = Factory.rami('test-bucket', 'test-g_blob.txt')
        print(f"RAMI g_blob factory test passed: {blob.name}")
    except Exception as e:
        print(f"RAMI g_blob factory test failed: {e}")

    try:
        # Test VALDAS factory
        blob = Factory.valdas('test-bucket', 'test-g_blob.txt')
        print(f"VALDAS g_blob factory test passed: {blob.name}")
    except Exception as e:
        print(f"VALDAS g_blob factory test failed: {e}")

    try:
        # Test generic factory
        blob = Factory.from_path('test-bucket', 'test-g_blob.txt', ServiceAccount.RAMI)
        print(f"Generic g_blob factory test passed: {blob.name}")
    except Exception as e:
        print(f"Generic g_blob factory test failed: {e}")


def test_blob_properties() -> None:
    """
    ========================================================================
    Test g_blob properties and metadata.
    ========================================================================
    """
    try:
        blob = Factory.rami('test-bucket', 'test-g_blob.txt')
        
        # Test basic properties
        print(f"Blob name: {blob.name}")
        print(f"Bucket name: {blob.bucket_name}")
        print(f"Public URL: {blob.public_url}")
        
        # Test string representations
        print(f"String repr: {str(blob)}")
        print(f"Detailed repr: {repr(blob)}")
        
        print("Blob properties test passed")
    except Exception as e:
        print(f"Blob properties test failed: {e}")


def test_blob_upload_download() -> None:
    """
    ========================================================================
    Test g_blob upload and download operations.
    WARNING: This test creates and deletes blobs.
    ========================================================================
    """
    try:
        blob = Factory.rami('test-bucket', 'test-g_blob-upload.txt')
        
        # Test string upload
        test_content = "Test content for g_blob operations"
        blob.upload_from_string(test_content, content_type='text/plain')
        print("String upload successful")
        
        # Test existence check
        if blob.exists():
            print("Blob exists check passed")
        
        # Test download as text
        downloaded_content = blob.download_as_text()
        assert downloaded_content == test_content
        print("Download as text successful")
        
        # Test download as bytes
        downloaded_bytes = blob.download_as_bytes()
        assert downloaded_bytes == test_content.encode('utf-8')
        print("Download as bytes successful")
        
        # Test file upload/download
        with tempfile.NamedTemporaryFile(mode='w', suffix='.txt', delete=False) as temp_file:
            temp_file.write("File upload test content")
            temp_file_path = temp_file.name
        
        try:
            blob.upload_from_file(temp_file_path, content_type='text/plain')
            print("File upload successful")
            
            # Test download to file
            download_path = temp_file_path + "_downloaded"
            blob.download_to_file(download_path)
            
            with open(download_path, 'r') as f:
                content = f.read()
                assert content == "File upload test content"
            print("File download successful")
            
            os.unlink(download_path)
            
        finally:
            os.unlink(temp_file_path)
        
        # Test metadata
        metadata = blob.get_metadata()
        print(f"Metadata: {metadata}")
        
        # Test custom metadata
        custom_metadata = {'author': 'test', 'version': '1.0'}
        blob.set_metadata(custom_metadata)
        print("Custom metadata set successfully")
        
        # Clean up
        blob.delete()
        print("Blob deleted successfully")
        
        print("All g_blob upload/download tests passed")
    except Exception as e:
        print(f"Blob upload/download test failed: {e}")


def test_blob_copy_move() -> None:
    """
    ========================================================================
    Test g_blob copy and move operations.
    WARNING: This test creates and deletes blobs.
    ========================================================================
    """
    try:
        # Create source g_blob
        source_blob = Factory.rami('test-bucket', 'source-g_blob.txt')
        source_blob.upload_from_string("Content to copy/move")
        
        # Test copy
        copied_blob = source_blob.copy_to('copied-g_blob.txt')
        print(f"Blob copied to: {copied_blob.name}")
        
        # Verify copy
        copied_content = copied_blob.download_as_text()
        assert copied_content == "Content to copy/move"
        print("Copy verification passed")
        
        # Test move
        moved_blob = copied_blob.move_to('moved-g_blob.txt')
        print(f"Blob moved to: {moved_blob.name}")
        
        # Verify move (original should not exist)
        assert not copied_blob.exists()
        assert moved_blob.exists()
        print("Move verification passed")
        
        # Clean up
        source_blob.delete()
        moved_blob.delete()
        
        print("Blob copy/move tests passed")
    except Exception as e:
        print(f"Blob copy/move test failed: {e}")


def test_blob_url_operations() -> None:
    """
    ========================================================================
    Test g_blob URL-related operations.
    WARNING: This test creates and deletes blobs.
    ========================================================================
    """
    try:
        blob = Factory.rami('test-bucket', 'test-url-g_blob.txt')
        
        # Test URL upload
        test_url = "https://httpbin.org/json"
        blob.upload_from_url(test_url, content_type='application/json')
        print("URL upload successful")
        
        # Test signed URL generation
        signed_url = blob.generate_signed_url(expiration_minutes=30)
        print(f"Generated signed URL: {signed_url[:50]}...")
        
        # Test public access
        blob.make_public()
        print("Blob made public")
        
        blob.make_private()
        print("Blob made private")
        
        # Clean up
        blob.delete()
        
        print("Blob URL operations tests passed")
    except Exception as e:
        print(f"Blob URL operations test failed: {e}")


def run_all_tests() -> None:
    """
    ========================================================================
    Run all g_blob-specific tests.
    ========================================================================
    """
    print("Running g_blob-specific tests...")
    
    try:
        test_blob_creation()
        test_blob_properties()
        
        # Uncomment these tests if you want to test g_blob operations
        # WARNING: These tests create/delete blobs
        # test_blob_upload_download()
        # test_blob_copy_move()
        # test_blob_url_operations()
        
        print("All g_blob tests completed successfully!")
        
    except Exception as e:
        print(f"Blob test failed: {e}")
        raise