from ._factory import Factory
from f_google._internal.auth import ServiceAccount
import tempfile
import os


def test_folder_creation() -> None:
    """
    ========================================================================
    Test folder creation using factory methods.
    ========================================================================
    """
    try:
        # Test RAMI factory
        folder = Factory.rami('test-bucket', 'test-folder/')
        print(f"RAMI folder factory test passed: {folder.path}")
    except Exception as e:
        print(f"RAMI folder factory test failed: {e}")

    try:
        # Test VALDAS factory
        folder = Factory.valdas('test-bucket', 'test-folder/')
        print(f"VALDAS folder factory test passed: {folder.path}")
    except Exception as e:
        print(f"VALDAS folder factory test failed: {e}")

    try:
        # Test root folder
        folder = Factory.root_rami('test-bucket')
        print(f"Root folder test passed: '{folder.path}'")
    except Exception as e:
        print(f"Root folder test failed: {e}")

    try:
        # Test generic factory
        folder = Factory.from_path('test-bucket', 'generic-folder/', ServiceAccount.RAMI)
        print(f"Generic folder factory test passed: {folder.path}")
    except Exception as e:
        print(f"Generic folder factory test failed: {e}")


def test_folder_properties() -> None:
    """
    ========================================================================
    Test folder properties and navigation.
    ========================================================================
    """
    try:
        folder = Factory.rami('test-bucket', 'documents/reports/')
        
        # Test basic properties
        print(f"Folder name: '{folder.name}'")
        print(f"Folder path: '{folder.path}'")
        print(f"Bucket name: '{folder.bucket_name}'")
        
        # Test parent folder
        parent = folder.parent
        if parent:
            print(f"Parent folder path: '{parent.path}'")
        
        # Test string representations
        print(f"String repr: {str(folder)}")
        print(f"Detailed repr: {repr(folder)}")
        
        print("Folder properties test passed")
    except Exception as e:
        print(f"Folder properties test failed: {e}")


def test_folder_operations() -> None:
    """
    ========================================================================
    Test folder operations like listing and navigation.
    ========================================================================
    """
    try:
        # Test root folder
        root_folder = Factory.root_rami('test-bucket')
        
        # Test listing operations
        files = root_folder.list_files(recursive=False)
        print(f"Files in root (non-recursive): {len(files)}")
        
        files_recursive = root_folder.list_files(recursive=True)
        print(f"Files in root (recursive): {len(files_recursive)}")
        
        folders = root_folder.list_folders()
        print(f"Subfolders in root: {len(folders)}")
        
        # Test subfolder creation
        subfolder = root_folder.create_subfolder('test-subfolder')
        print(f"Created subfolder: {subfolder.path}")
        
        # Test folder navigation
        if folders:
            first_folder = root_folder.get_subfolder(folders[0].rstrip('/').split('/')[-1])
            print(f"Navigated to subfolder: {first_folder.path}")
        
        # Test folder properties
        print(f"Root folder size: {root_folder.get_size()} bytes")
        print(f"Root folder file count: {root_folder.get_file_count()}")
        print(f"Root folder total items: {len(root_folder)}")
        
        print("Folder operations test passed")
    except Exception as e:
        print(f"Folder operations test failed: {e}")


def test_folder_file_operations() -> None:
    """
    ========================================================================
    Test folder file operations.
    WARNING: This test creates and deletes files.
    ========================================================================
    """
    try:
        folder = Factory.rami('test-bucket', 'test-folder/')
        
        # Test string upload
        test_content = "Test content for folder operations"
        blob = folder.upload_string(test_content, 'test-file.txt')
        print(f"String uploaded to folder: {blob.name}")
        
        # Test file existence
        if 'test-file.txt' in folder:
            print("File exists check passed")
        
        # Test file retrieval
        file_blob = folder.get_file('test-file.txt')
        content = file_blob.download_as_text()
        assert content == test_content
        print("File retrieval test passed")
        
        # Test file operations with temp file
        with tempfile.NamedTemporaryFile(mode='w', suffix='.txt', delete=False) as temp_file:
            temp_file.write("Temp file content")
            temp_file_path = temp_file.name
        
        try:
            # Test file upload
            uploaded_blob = folder.upload_file(temp_file_path, 'uploaded-file.txt')
            print(f"File uploaded to folder: {uploaded_blob.name}")
            
            # Test file download
            download_path = temp_file_path + "_downloaded"
            folder.download_file('uploaded-file.txt', download_path)
            
            with open(download_path, 'r') as f:
                content = f.read()
                assert content == "Temp file content"
            print("File download test passed")
            
            # Clean up
            folder.delete_file('uploaded-file.txt')
            os.unlink(download_path)
            
        finally:
            os.unlink(temp_file_path)
        
        # Clean up
        folder.delete_file('test-file.txt')
        
        print("Folder file operations test passed")
    except Exception as e:
        print(f"Folder file operations test failed: {e}")


def test_folder_sync_operations() -> None:
    """
    ========================================================================
    Test folder sync operations with local directories.
    WARNING: This test creates and deletes files and folders.
    ========================================================================
    """
    try:
        folder = Factory.rami('test-bucket', 'sync-test/')
        
        # Create temporary local directory structure
        with tempfile.TemporaryDirectory() as temp_dir:
            # Create test files
            os.makedirs(os.path.join(temp_dir, 'subfolder'), exist_ok=True)
            
            with open(os.path.join(temp_dir, 'file1.txt'), 'w') as f:
                f.write("File 1 content")
            
            with open(os.path.join(temp_dir, 'subfolder', 'file2.txt'), 'w') as f:
                f.write("File 2 content")
            
            # Test sync from local
            folder.sync_from_local(temp_dir, recursive=True)
            print("Sync from local completed")
            
            # Verify files were uploaded
            files = folder.list_files(recursive=True)
            print(f"Files after sync: {len(files)}")
            
            # Test sync to local
            download_dir = os.path.join(temp_dir, 'downloaded')
            folder.sync_to_local(download_dir, recursive=True)
            print("Sync to local completed")
            
            # Verify files were downloaded
            assert os.path.exists(os.path.join(download_dir, 'file1.txt'))
            assert os.path.exists(os.path.join(download_dir, 'subfolder', 'file2.txt'))
            print("Sync verification passed")
            
            # Clean up remote files
            folder.delete_folder(recursive=True)
            
        print("Folder sync operations test passed")
    except Exception as e:
        print(f"Folder sync operations test failed: {e}")


def test_folder_walk() -> None:
    """
    ========================================================================
    Test folder walking functionality.
    ========================================================================
    """
    try:
        root_folder = Factory.root_rami('test-bucket')
        
        # Test walking through folder structure
        walked_folders = []
        for folder_path, subfolders, files in root_folder.walk():
            walked_folders.append((folder_path, len(subfolders), len(files)))
            if len(walked_folders) > 10:  # Limit to avoid too much output
                break
        
        print(f"Walked through {len(walked_folders)} folders")
        for folder_path, subfolder_count, file_count in walked_folders[:5]:
            print(f"  {folder_path}: {subfolder_count} subfolders, {file_count} files")
        
        print("Folder walk test passed")
    except Exception as e:
        print(f"Folder walk test failed: {e}")


def run_all_tests() -> None:
    """
    ========================================================================
    Run all folder-specific tests.
    ========================================================================
    """
    print("Running folder-specific tests...")
    
    try:
        test_folder_creation()
        test_folder_properties()
        test_folder_operations()
        test_folder_walk()
        
        # Uncomment these tests if you want to test folder operations
        # WARNING: These tests create/delete files and folders
        # test_folder_file_operations()
        # test_folder_sync_operations()
        
        print("All folder tests completed successfully!")
        
    except Exception as e:
        print(f"Folder test failed: {e}")
        raise