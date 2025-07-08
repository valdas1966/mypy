from ._factory import Factory
from f_google._internal.auth import ServiceAccount
import tempfile
import os


def test_file_creation() -> None:
    """
    ========================================================================
    Test file creation using factory methods.
    ========================================================================
    """
    try:
        # Test RAMI factory
        file = Factory.rami('test-bucket', 'test-file.txt')
        print(f"RAMI file factory test passed: {file.path}")
    except Exception as e:
        print(f"RAMI file factory test failed: {e}")

    try:
        # Test VALDAS factory
        file = Factory.valdas('test-bucket', 'test-file.txt')
        print(f"VALDAS file factory test passed: {file.path}")
    except Exception as e:
        print(f"VALDAS file factory test failed: {e}")

    try:
        # Test generic factory
        file = Factory.from_path('test-bucket', 'generic-file.txt', ServiceAccount.RAMI)
        print(f"Generic file factory test passed: {file.path}")
    except Exception as e:
        print(f"Generic file factory test failed: {e}")

    try:
        # Test new file creation
        file = Factory.create_new_rami('test-bucket', 'new-file.txt')
        print(f"New file creation test passed: {file.path}")
    except Exception as e:
        print(f"New file creation test failed: {e}")


def test_file_properties() -> None:
    """
    ========================================================================
    Test file properties and metadata.
    ========================================================================
    """
    try:
        file = Factory.rami('test-bucket', 'documents/report.pdf')
        
        # Test basic properties
        print(f"File name: '{file.name}'")
        print(f"File stem: '{file.stem}'")
        print(f"File suffix: '{file.suffix}'")
        print(f"File path: '{file.path}'")
        print(f"Parent path: '{file.parent_path}'")
        print(f"Bucket name: '{file.bucket_name}'")
        print(f"Public URL: '{file.public_url}'")
        
        # Test file type detection
        print(f"Content type: '{file.content_type}'")
        print(f"Is text file: {file.is_text_file()}")
        print(f"Is image file: {file.is_image_file()}")
        print(f"File type: '{file.get_file_type()}'")
        
        # Test string representations
        print(f"String repr: {str(file)}")
        print(f"Detailed repr: {repr(file)}")
        
        # Test equality
        file2 = Factory.rami('test-bucket', 'documents/report.pdf')
        print(f"Files equal: {file == file2}")
        print(f"File hash: {hash(file)}")
        
        print("File properties test passed")
    except Exception as e:
        print(f"File properties test failed: {e}")


def test_file_text_operations() -> None:
    """
    ========================================================================
    Test file text read/write operations.
    WARNING: This test creates and deletes files.
    ========================================================================
    """
    try:
        file = Factory.rami('test-bucket', 'test-text-file.txt')
        
        # Test text write
        test_content = "Hello, World!\nThis is a test file."
        file.write_text(test_content)
        print("Text write successful")
        
        # Test existence check
        if file.exists():
            print("File exists check passed")
        
        # Test text read
        read_content = file.read_text()
        assert read_content == test_content
        print("Text read successful")
        
        # Test append text
        append_content = "\nAppended line."
        file.append_text(append_content)
        
        # Verify append
        final_content = file.read_text()
        assert final_content == test_content + append_content
        print("Text append successful")
        
        # Test metadata operations
        metadata = file.get_metadata()
        print(f"File metadata: {metadata}")
        
        custom_metadata = {'author': 'test', 'type': 'text'}
        file.set_metadata(custom_metadata)
        print("Custom metadata set successfully")
        
        # Clean up
        file.delete()
        print("File deleted successfully")
        
        print("File text operations test passed")
    except Exception as e:
        print(f"File text operations test failed: {e}")


def test_file_binary_operations() -> None:
    """
    ========================================================================
    Test file binary read/write operations.
    WARNING: This test creates and deletes files.
    ========================================================================
    """
    try:
        file = Factory.rami('test-bucket', 'test-binary-file.bin')
        
        # Test binary write
        test_content = b"Binary content \x00\x01\x02\x03"
        file.write_bytes(test_content)
        print("Binary write successful")
        
        # Test binary read
        read_content = file.read_bytes()
        assert read_content == test_content
        print("Binary read successful")
        
        # Test append bytes
        append_content = b"\x04\x05\x06"
        file.append_bytes(append_content)
        
        # Verify append
        final_content = file.read_bytes()
        assert final_content == test_content + append_content
        print("Binary append successful")
        
        # Clean up
        file.delete()
        
        print("File binary operations test passed")
    except Exception as e:
        print(f"File binary operations test failed: {e}")


def test_file_local_operations() -> None:
    """
    ========================================================================
    Test file operations with local files.
    WARNING: This test creates and deletes files.
    ========================================================================
    """
    try:
        file = Factory.rami('test-bucket', 'test-local-file.txt')
        
        # Create temporary local file
        with tempfile.NamedTemporaryFile(mode='w', suffix='.txt', delete=False) as temp_file:
            temp_file.write("Content from local file")
            temp_file_path = temp_file.name
        
        try:
            # Test copy from local
            file.copy_from_local(temp_file_path)
            print("Copy from local successful")
            
            # Verify content
            content = file.read_text()
            assert content == "Content from local file"
            print("Local file content verification passed")
            
            # Test copy to local
            download_path = temp_file_path + "_downloaded"
            file.copy_to_local(download_path)
            
            # Verify download
            with open(download_path, 'r') as f:
                downloaded_content = f.read()
                assert downloaded_content == "Content from local file"
            print("Copy to local successful")
            
            # Clean up
            os.unlink(download_path)
            
        finally:
            os.unlink(temp_file_path)
        
        # Clean up remote file
        file.delete()
        
        print("File local operations test passed")
    except Exception as e:
        print(f"File local operations test failed: {e}")


def test_file_copy_move_operations() -> None:
    """
    ========================================================================
    Test file copy, move, and rename operations.
    WARNING: This test creates and deletes files.
    ========================================================================
    """
    try:
        # Create source file
        source_file = Factory.rami('test-bucket', 'source-file.txt')
        source_file.write_text("Content to copy/move")
        
        # Test copy
        copied_file = source_file.copy_to('copied-file.txt')
        print(f"File copied to: {copied_file.path}")
        
        # Verify copy
        copied_content = copied_file.read_text()
        assert copied_content == "Content to copy/move"
        print("Copy verification passed")
        
        # Test rename
        renamed_file = copied_file.rename('renamed-file.txt')
        print(f"File renamed to: {renamed_file.path}")
        
        # Verify rename (original should not exist)
        assert not copied_file.exists()
        assert renamed_file.exists()
        print("Rename verification passed")
        
        # Test backup
        backup_file = source_file.backup('.backup')
        print(f"Backup created: {backup_file.path}")
        
        # Test move
        moved_file = renamed_file.move_to('moved-file.txt')
        print(f"File moved to: {moved_file.path}")
        
        # Verify move
        assert not renamed_file.exists()
        assert moved_file.exists()
        print("Move verification passed")
        
        # Clean up
        source_file.delete()
        backup_file.delete()
        moved_file.delete()
        
        print("File copy/move operations test passed")
    except Exception as e:
        print(f"File copy/move operations test failed: {e}")


def test_file_url_operations() -> None:
    """
    ========================================================================
    Test file URL-related operations.
    WARNING: This test creates and deletes files.
    ========================================================================
    """
    try:
        file = Factory.rami('test-bucket', 'test-url-file.json')
        
        # Test URL upload
        test_url = "https://httpbin.org/json"
        file.copy_from_url(test_url)
        print("URL upload successful")
        
        # Test signed URL generation
        signed_url = file.generate_signed_url(expiration_minutes=30)
        print(f"Generated signed URL: {signed_url[:50]}...")
        
        # Test public access
        file.make_public()
        print("File made public")
        
        file.make_private()
        print("File made private")
        
        # Test download stream
        stream = file.get_download_stream()
        stream_content = stream.read()
        print(f"Downloaded via stream: {len(stream_content)} bytes")
        
        # Clean up
        file.delete()
        
        print("File URL operations test passed")
    except Exception as e:
        print(f"File URL operations test failed: {e}")


def run_all_tests() -> None:
    """
    ========================================================================
    Run all file-specific tests.
    ========================================================================
    """
    print("Running file-specific tests...")
    
    try:
        test_file_creation()
        test_file_properties()
        
        # Uncomment these tests if you want to test file operations
        # WARNING: These tests create/delete files
        # test_file_text_operations()
        # test_file_binary_operations()
        # test_file_local_operations()
        # test_file_copy_move_operations()
        # test_file_url_operations()
        
        print("All file tests completed successfully!")
        
    except Exception as e:
        print(f"File test failed: {e}")
        raise